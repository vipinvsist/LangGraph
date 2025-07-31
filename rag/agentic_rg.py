from unittest import result
from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from operator import add as add_messages
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.tools import tool


load_dotenv()

llm = ChatOpenAI(model = "gpt-4o-mini", temperature=0.3)
embeddings = OpenAIEmbeddings(
    model = "text-embedding-3-small"
)

pdf_path = r"C:\Users\Vipin Vashisth\Downloads\Hyperspectral_final_pdf.pdf"

if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF file not found: {pdf_path}")

pdf_loader = PyPDFLoader(pdf_path)


try:
    pages = pdf_loader.load()
    print(f"PDF HAS BEEN LOADED AND HAS {len(pages)} pages")


except Exception as e:
    print(f"Error in loaing PDF: {e}")
    raise

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

pages_split = text_splitter.split_documents(pages)

persist_directory = r"C:\Users\Vipin Vashisth\Desktop\Langgraph\rag"
collection_name = r"Hyperspectral_final"

if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)
try:
    vectorstore = Chroma.from_documents(
        documents=pages_split,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    print(f"Created ChromaDB vector store!")
except Exception as e:
    print(f"Error while setting up chroma db: {str(e)}")
print("After Chroma")


# except Exception as e:
#     print(f"Error while setting up chroma db: {str(e)}")
#     raise
retriver = vectorstore.as_retriever(
    search_type = "similarity",
    search_kwargs = {'k':5}

)

@tool
def retriver_tool(query:str)->str:
    """
    
    """
    docs = retriver.invoke(query)

    if not docs:
        return "I found no relavent information in the Hyperspectroscopy document."
    
    results  =[]

    for i, doc in enumerate(docs):
        results.append(f"document {i+1}:\n{doc.page_content}")

    return "\n\n".join(results)

tools  = [retriver_tool]
llm = llm.bind_tools(tools)

class AgentState(TypedDict):
    message: Annotated[Sequence[BaseMessage], add_messages]


def should_continue(state: AgentState):
    """ Check if the last message contains the tools calls?"""

    result = state['message'][-1]
    return hasattr(result,"tool_calls") and len(result.tool_calls) >0

system_prompt = """
You are an intelligent AI assistant who answers questions about Stock Market Performance in 2024 based on the PDF document loaded into your knowledge base.
Use the retriever tool available to answer questions about the stock market performance data. You can make multiple calls if needed.
If you need to look up some information before asking a follow up question, you are allowed to do that!
Please always cite the specific parts of the documents you use in your answers.
"""

tools_dict = {our_tool.name: our_tool for our_tool in tools}

def call_llm(state:AgentState):
    """Function to call the LLM witht the Current State"""
    message = list(state['message'])
    message = [SystemMessage(content=system_prompt)]+message
    message = llm.invoke(message)
    return {"message": [message]}


# Retriver Agent

def take_action(state:AgentState)-> AgentState:
    """Ececute the releavent tool call from the LLM's response"""

    tool_calls =state['message'][-1].tool_calls
    results=[]
    for t in tool_calls:
        print(f"Calling Tool: {t['name']} with query: {t['args'].get('query','No query Provided')}")
        if not t['name'] in tools_dict:      # check for the valid tool
            print(f"\nTool: {t['name']} does not exist.")
            result = "Incorrect Tool Name, Please Retry and Select tool from the list of tools available."

        else:
            result = tools_dict[t['name']].invoke(t['args'].get('query',""))
            print(f"Result length: {len(str(result))}")

        #Append the Tool Message
        
        results.append(ToolMessage(tool_call_id=t['id'], name=t['name'],content=str(result)))

    print("Tools Execution Complete. Back to the model!")
    return {"message": results}

graph=StateGraph(AgentState)
graph.add_node("llm",call_llm)
graph.add_node("retriver_agent",take_action)

graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        True: "retriver_agent",
        False: END
    }
)
graph.add_edge("retriver_agent",llm)
graph.set_entry_point("llm")


rag_agent = graph.compile()


def running_agent():
    print(("\n=== RAG AGENT"))

    while True:
        user_input = input("\nWhat is your question: ")
        if user_input.lower() in ["exit","quit"]:
            break

        message = [HumanMessage(content=user_input)]
        result = rag_agent.invoke({"message":message})
        print("\n============Answer============")

        print(result['messages'][-1].content)


running_agent()
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

pdf_path = r"C:\Users\Vipin Vashisth\Downloads\Hyperspectral image analysis with Python made easy _ by Antón Garcia _ Abraia _ Feb, 2021 _ Medium _ Abraia.pdf"

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

page_split = text_splitter.split_documents(pages)

persist_directory = r"C:\Users\Vipin Vashisth\Desktop\Langgraph\rag"
collection_name = "Hyperspectral_name"

if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)


try:
    vectorstore = Chroma.from_documents(
        documents=page_split,
        embeddings = embeddings,
        persist_directory= persist_directory,
        collection_name=collection_name
    )
    print(f"Created ChromaDB vector store!")

except Exception as e:
    print(f"Error while setting up chroma db: {str(e)}")
    raise
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
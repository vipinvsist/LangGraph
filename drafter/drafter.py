"""
AIM: create an AI Agentic System that canspeed up drafting documents, emails, etc. 

The AI Agentic System should have Human-AI Collaboration meaning the Human should be able to able to provide continuous feedback and 
the AI Agent should stop when the Human is happy with the draft. 
The system should also be fast and be able to save the drafts.
"""

from email import message
from typing import Annotated, TypedDict, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

# Global Varible
document_content = ""

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]

@tool
def update(content: str)->str:
    """ Update the document with provided content"""

    global document_content
    document_content = content
    return f"Document has been updated sucessfully! The current content is \n{document_content}"

@tool 
def save(filename:str)-> str:
    """
    Save the current document to a text file and finish the process

    Args: 
        filename: Name for the text file.
    """
    global document_content

    if not filename.endswith(".txt"):
        filename = f"{filename}.txt"

    try:
        with open(filename,"w") as file:
            file.write(document_content)

        print(f"Document has been saved to {filename}")
        return f"Document has been saved sucessfully to '{filename}'!"
    except Exception as e:
        return f" Error while saving the file: {str(e)}"
    
tools  = [update, save]
model = ChatOpenAI(model = "gpt-4o-mini").bind_tools(tools)

def our_agent(state: AgentState)-> str:
    system_prompt = SystemMessage(content=f"""
    You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.
    - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
    - If the user wants to save and finish, you need to use the 'save' tool.
    - Make sure to always show the current document state after modifications.
    The current document content is:{document_content}
""")
    
    if not state['messages']:
        user_input = "I'm redy to help you to update a document. What would you like to create?\n"
        user_message = HumanMessage(content=user_input)

    else:
        user_input = input("What would you like to do with this documment?\n")
        print(f"\n User: {user_input}")

        user_message=HumanMessage(content=user_input)


    all_messages = [system_prompt] + list(state['messages'])+[user_message]
    response = model.invoke(all_messages)


    print(f"\n AI: {response.content}")
    if hasattr(response,"tool_calls") and response.tool_calls:
        print(f"Using tools: {[tc['name'] for tc in response.tool_calls]}")
        
    return {"messages": list(state['messages'])+ [user_message, response]}


def should_continue(state:AgentState)-> AgentState:
    """Determine if we should continue or end the process"""

    messages= state['messages']

    if not messages:
        return "continue"
    
    # This for the recent tool messages
    for message in reversed(messages):
        # and check if this is a ToolMessage resulting from save
        if (isinstance(message, ToolMessage) and
            "saved" in message.content.lower()
            and "document" in message.content.lower()):
            return "end"  # goes to end node
        
    return "continue"

def print_messsage(messages):
    """This function is to print messages in a readable format"""

    if not messages:
        return

    for message in messages[-3:]:
        if isinstance(message,ToolMessage):
            print(f" \n TOOL RESULT: {message.content}")


graph = StateGraph(AgentState)

graph.add_node("agent", our_agent)
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("agent")

graph.add_edge("agent","tools")

graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue":"agent",
        "end": END
    }
)

app = graph.compile()

def run_document_agent():
    print("\n=============Drafter============")
    state = {"messages": []}

    for step in app.stream(state, stream_mode = "values"):
        if "messages" in step:
            print_messsage(step['messages'])

    print("\n==============Dratfer Finished============")



if __name__ == "__main__":
    run_document_agent()
"""AIM:  Create a robust ReAct Agent!
Learn how to create REACT graph
Work with different types of Messages like ToolMessages
Test out roubstness of our graph
"""

from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage   # Foundational class for all message tpes in Langgraph
from langchain_core.messages import ToolMessage   # Passes data back to LLM after it calls a tool such as the content and the tool_call_is
from langchain_core.messages import SystemMessage # Message for providing instructions to the LLM
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

load_dotenv()
# Annoted - provides additional context without affecting the tpe itself
# email = Annotated[str,"This should be in proper email format"]
# print(email.__metadata__)


# Sequence - To automatically handle the state updates for sequences such as adding a new messages to a chat history

# add_messages a reducer Function
# Rule that controls how updates from nodes are cmobined with the existing state
# Tells us how to merge new data into the current state
# Without a reducer, updates would have replaced the existing value entirely

# without a reducer

# state = {"messages": ["Hi"]}
# update = {"messages": ['Nice to meet you']}
# new_state = {"message":["Nice to meet you"]}

# # With a Reducer
# state = {"messages": ["Hi"]}
# update = {"messages": ['Nice to meet you']}
# new_state = {"message":["Hi","Nice to meet you"]}

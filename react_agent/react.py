"""AIM:  Create a robust ReAct Agent!
Learn how to create REACT graph
Work with different types of Messages like ToolMessages
Test out roubstness of our graph
"""

from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage   # Foundational class for all message tpes in Langgraph
from langchain_core.messages import ToolMessage   # Passes data back to LLM after it calls a tool suchas the content and the
from langchain_core.messages import SystemMessage # Message for providing instructions to the LLM
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

load_dotenv()
# Annoted - provides additional context without affecting the tpe itself
# email = Annotated[str,"This should be in proper email format"]
# print(email.__metadata__)


# Sequence - To automatically handle the state updates for sequences such as adding a new messages to a chat history

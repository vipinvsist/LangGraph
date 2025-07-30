"""
AIM: create an AI Agentic System that canspeed up drafting documents, emails, etc. 

The AI Agentic System should have Human-AI Collaboration meaning the Human should be able to able to provide continuous feedback and 
the AI Agent should stop when the Human is happy with the draft. 
The system should also be fast and be able to save the drafts.
"""

from typing import Annotated, TypedDict, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

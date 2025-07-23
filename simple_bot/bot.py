"""
Aim: To integrate LLMs with the graphs
Define state structure with a list of HumanMessage objects
Initalize GPT-4o-mini model using Langchain's ChatOpenAI
Sending and handling different types of messages
Building and compiling the graph of the Agent
"""
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import os
load_dotenv()

class AgentState(TypedDict):
    message: List[HumanMessage]

llm = ChatOpenAI(model="gpt-4o-mini")


def process(state: AgentState)->AgentState:
    response = llm.invoke(state['message'])
    print(f"\nAI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)

agent = graph.compile()
with open("graph.png", "wb") as f:
    f.write(agent.get_graph().draw_mermaid_png())

os.startfile("graph.png")


user_input = input("Who's this..?")
# agent.invoke({'message':[HumanMessage(content=user_input)]})
while user_input !="exit":
    agent.invoke({'message':[HumanMessage(content=user_input)]})
    user_input = input("Enter: ")
    
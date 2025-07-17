import matplotlib.pyplot as plt
from typing import TypedDict, final
from langgraph.graph import StateGraph
import os

class AgentState(TypedDict):
    name: str
    age: str
    final: str

def first_node(state:AgentState) ->AgentState:
    """This is the firt node of our sequence"""
    state['final'] = f"Hi, {state['name']}"

    return state

def second_node(state:AgentState)-> AgentState:
    "This is the second node of our sequence"
    state['final']= state['final']+ f", you are {state['age']} years old."
    return state

graph = StateGraph(AgentState)

graph.add_node("first_node", first_node)
graph.add_node("second_node",second_node)
graph.set_entry_point("first_node")
graph.set_finish_point("second_node")

graph.add_edge("first_node","second_node")

app = graph.compile()
result = app.invoke({"name": "Vipin","age":"23"})
print(result['final'])

with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

os.startfile("graph.png")
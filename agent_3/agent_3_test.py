from typing import TypedDict
from langgraph.graph import StateGraph
import os

from more_itertools import first

class AgentState(TypedDict):
    name: str
    age: str
    final: str

def first_node(state: AgentState)->AgentState:
    state['final'] = f"Hi, {state['name']}, how are you?"
    return state

def second_node(state: AgentState)-> AgentState:
    state['final'] = state['final'] + f" you are {state['age']} years old."
    return state

def third_node(state:AgentState)-> AgentState:
    state['final'] = state['final']+ f". As you have mentioned you are skilled with Machine Learning and AI domains."

    return state

graph = StateGraph(AgentState)
graph.set_entry_point("first_node")
graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.add_node("third_node", third_node)
graph.add_edge("first_node","second_node")
graph.add_edge("second_node","third_node")
graph.set_finish_point("third_node")

app = graph.compile()

result = app.invoke({"name": 'Vipin', "age": "23"})

print(result['final'])

with open("graph_test.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

os.startfile("graph_test.png")
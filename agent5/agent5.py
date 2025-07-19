"""
Aim: Implement looping
Implement looping to route up the data back to the nodes
Creating a single conditional edge to handle decision-making and control graph flow.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import random
import os


class AgentState(TypedDict):
    name: str
    nums: list[int]
    counter: int

def greet_node(state:AgentState)-> AgentState:
    state['name'] = f"Hi, there, {state['name']}"
    state['counter'] = 0
    return state

def random_node(state:AgentState)->AgentState:
    state['nums'].append(random.randint(0,10))
    state['counter'] +=1
    return state

def cont_edge(state:AgentState)->AgentState:
    if state['counter']<5:
        print(f"Entering Loop!!.., {state['counter']}")
        return "loop"
    else:
        return "exit"
    
graph = StateGraph(AgentState)

graph.add_node("greeting_node", greet_node)
graph.add_node("random_node", random_node)

graph.add_edge("greeting_node","random_node")

graph.add_conditional_edges(
    "random_node",
    cont_edge,
    {
        "loop": "random_node",
        "exit": END
    }
)
graph.set_entry_point("greeting_node")
app = graph.compile()
with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

os.startfile("graph.png")

result = app.invoke({"name": "Vipin Vashsith", "nums":[], "counter":-23})
print(result)
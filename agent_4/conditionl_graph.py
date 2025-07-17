"""
Aim: How to use add_conditional_edges() 
Use conditional nodes to route the flow of logic to different data nodes
Use of Start and End nodes to manage entry and exit points
Create router node to help in decision making
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import os
class AgentState(TypedDict):
    num1: int
    operation: str
    num2: int
    finalNumber: int

def adder(state:AgentState)-> AgentState:
    "adds 2 number"
    state['finalNumber'] = state['num1'] + state['num2']
    return state

def subtractor(state: AgentState)-> AgentState:
    "sub 2 numbers"
    state['finalNumber']=  state['num1'] - state['num2']
    return state

def decide_next_node(state: AgentState):
    if state['operation'] == "+":
        return "addition_operation"
    elif state['operation']== "-":
        return "subtraction_operation"
    
graph = StateGraph(AgentState)

graph.add_node("add_node",adder)
graph.add_node("sub_node",subtractor)
graph.add_node("router",lambda state:state)
graph.add_edge(START,"router")
graph.add_conditional_edges(
    "router",
    decide_next_node,
    {  # Edge: Node
        "addition_operation":"add_node",
        "subtraction_operation":"sub_node"
    }
)
graph.add_edge("add_node",END)
graph.add_edge("sub_node",END)

app = graph.compile()

with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

os.startfile("graph.png")


initial_state_1 = AgentState(num1 = 10, num2=32, operation="-")
print(app.invoke(initial_state_1))

initial_state_2 = AgentState(num1 = 10, num2=32, operation="+")
print(app.invoke(initial_state_2))
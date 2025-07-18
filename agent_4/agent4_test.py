from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import os
class AgentState(TypedDict):
    num1: int
    num2: int
    num3: int
    num4: int
    finalnum1: int
    finalnum2: int
    operation1:str
    operation2:str

def first_node(state:AgentState)-> AgentState:
    state['finalnum1'] = f"The sum of num1 and num2 is {state['num1']+ state['num2']} "
    return state

def second_node(state:AgentState)-> AgentState:
    state['finalnum1'] = f"The sub of num1 and num2 is {state['num1']- state['num2']} "
    return state
    
def third_node(state:AgentState)-> AgentState:
    state['finalnum2'] = f"The add of num3 and num4 is {state['num3']+ state['num4']} "
    return state

def fourth_node(state:AgentState)-> AgentState:
    state['finalnum2'] = f"The sub of num3 and num4 is {state['num3']- state['num4']} "
    return state

def decision_node1(state:AgentState)->AgentState:
    if state['operation1']=="+":
        return "addition_operation"
    elif state['operation1']=="-":
        return "subtraction_operation"
    
def decision_node2(state:AgentState)->AgentState:
    if state['operation2']=="+":
        return "addition_operation"
    elif state['operation2']=="-":
        return "subtraction_operation"
    

graph = StateGraph(AgentState)

graph.add_node("first_node",first_node)
graph.add_node("second_node",second_node)
graph.add_node("router1",lambda state:state)
graph.add_node("third_node",third_node)
graph.add_node("fourth_node",fourth_node)
graph.add_node("router2",lambda state:state)
graph.add_edge(START, "router1")
graph.add_conditional_edges(
    "router1",
    decision_node1,
    {
        "addition_operation": "first_node",
        "subtraction_operation": "second_node",

    }
)
graph.add_edge("first_node", "router2")
graph.add_edge("second_node", "router2")

graph.add_conditional_edges(
    "router2",
    decision_node2,
    {
        "addition_operation": "third_node",
        "subtraction_operation": "fourth_node",

    }
)
graph.add_edge("third_node",END)
graph.add_edge("fourth_node", END)

# graph.add_edge("third_node", third_node)
# graph.add_edge("fourth_node",fourth_node)



app = graph.compile()

with open("graph_test.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

os.startfile("graph_test.png")


initial_state_1 = AgentState(num1 = 10, num2=32,num3=32, num4=21, operation1="-",operation2="+")
print(app.invoke(initial_state_1))


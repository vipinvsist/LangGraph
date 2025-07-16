"""
Hello World Graph
Define Agent state
Set up with basic LangGraph structure
Understand how data flow through a single node in LangGraph
"""
from typing import Dict, TypedDict
from langgraph.graph import StateGraph           #framework that helps in designing the flow of tasks in your application

# AgentState - shared data structure that keeps tracks of the information as your application runs

class AgentState(TypedDict):
    message: str

def greeting_node(state: AgentState) -> AgentState:
    "Simple node that ads a greeting message to the state"
    state['message'] = "Hey " + state['message'] + ", how are you doing?"
    return state


graph=StateGraph(AgentState)
graph.add_node("Greeter",greeting_node)
graph.set_entry_point("Greeter")
graph.set_finish_point("Greeter")

app = graph.compile()
result = app.invoke({"message": "Vipin"})
print(result['message'])


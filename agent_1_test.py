"Assignment"
from typing import Dict, TypedDict
from langgraph.graph import StateGraph

class Agentstate(TypedDict):
    name: str

def agent_initalizer(state: Agentstate) -> Agentstate:
    state['name'] = state['name'] + ", you're doing an amazing job in learning!"
    return state

graph = StateGraph(Agentstate)

graph.add_node("advisor",agent_initalizer)
graph.set_entry_point("advisor")
graph.set_finish_point("advisor")

app = graph.compile()
result = app.invoke({"name":"Vipin"})

print(result['name'])
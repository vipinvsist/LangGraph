"""
AIM: To handle Multiple inputs
Define a more complex agentstate
Create a processing node that performs the operations on list data
St up a LangGraph that precessed and output computed results.
Invoke the graph to get the outputs


"""

from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph

class Agentstate(TypedDict):
    values: List[int]
    name: str
    result: str

def process_vlaues(state: Agentstate) -> Agentstate:
    "This function handles multiple different inputs"
    print(state)
    state['result']= f"Hi there {state['name']}! Your sum  is = {sum(state['values'])}"
    return state

graph = StateGraph(Agentstate)
graph.add_node("processor", process_vlaues)
graph.set_finish_point("processor")
graph.set_entry_point("processor")
app=graph.compile()
result = app.invoke({"values":[1,2,3,4], "name":"Ishu"})

print(result['result'])

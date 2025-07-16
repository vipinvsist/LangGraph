from sre_parse import State
from typing import TypedDict, List
from langgraph.graph import StateGraph


class Agentstate(TypedDict):
    nums: List[int]
    name: str
    values:str

def report_agent(state:Agentstate)-> Agentstate:
    state['values'] = f"Hi {state['name']}, your answer is: {sum(state['nums'])}"
    return state

graph = StateGraph(Agentstate)
graph.add_node("agent",report_agent)
graph.set_finish_point("agent")
graph.set_entry_point("agent")
app = graph.compile()

result  = app.invoke({"nums":[43,24,52,53,55], "name": "Vipin"})

print(result['values'])
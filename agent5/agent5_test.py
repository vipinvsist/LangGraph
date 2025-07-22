"""
Make the graph on the right! You need to implement an Automatic Higher or Lower
Game.
Set the bounds to between 1 to 20. The Graph has to keep guessing (max number of
guesses is 7) where if the guess is correct, then it stops, but if not we keep looping until
we hit the max limit of 7.
Each time a number is guessed, the hint node should say higher or lower and the graph
should account for this information and guess the next guess accordingly.
Input: {"player_name": "Student", "guesses": [], "attempts": 0, "lower_bound": 1,
"upper_bound": 20}
Hint: It will need to adjust its bounds after every guess based on the hint provided by the
hint node.
"""

from typing import TypedDict
from langgraph.graph import START, END, StateGraph
import os
import random

class AgentState(TypedDict):
    name: str
    target: int
    guess: list[int]
    attempts: int
    lower_bound: int
    upper_bound: int


def setup_node(state:AgentState)-> AgentState:
    state['name'] = f"Hi, {state['name']}, how are you?"
    state['attempts'] = 0
    return state

def random_guesser(state:AgentState)-> AgentState:
    state['guess'].append(random.randint(0,10))
    state['attempts']+=1
    return state

def checker(state:AgentState)->AgentState:
    if state['attempts']<=7:
        print(f"entering loop, {state['attempts']}!!")
        if state['guess'] and state['guess'][-1] == state['target']:
            print(f"You have made a correct guess: {state['guess'][-1]} == {state['target']}")
            return "exit"
        else:
            return "loops"
    else:
        return "exit"
def hint_node(state:AgentState)->AgentState:
    if not state['guess']:
        print("No guess yet — skipping hint.")
        return state
    last_guess = state['guess'][-1]
    target = state['target']
    if last_guess < target:
        print(f"Hint: Try a higher number than {last_guess}")
    elif last_guess > target:
        print(f"Hint: Try a lower number than {last_guess}")
    else:
        print("Correct guess!")
    return state
     
graph = StateGraph(AgentState)

graph.add_node("setup_node", setup_node)
graph.add_node("Guess", random_guesser)
graph.add_edge("setup_node","Guess")
graph.add_node("hint",hint_node)

graph.add_conditional_edges(
    "Guess",
    checker,
    {
        "loops": "hint",
        "exit": END
    }
)
graph.add_edge("hint", "Guess")

graph.set_entry_point("setup_node")
app = graph.compile()
with open("graph_test.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

os.startfile("graph_test.png")


result = app.invoke({"name":"Vipin", "target":8,"attempts":0,"guess":[],"lower_bound":1,"upper_bound":20})

print(result)
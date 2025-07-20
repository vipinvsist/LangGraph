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
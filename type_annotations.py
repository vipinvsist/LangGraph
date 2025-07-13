 #1. Type Dictionaries
from typing import TypedDict, Union, Optional, Any
 
class movie(TypedDict):
    name: str
    year: int


# print(movie(name=134, year= 2025))
print(movie(name="Avengers Endgame", year= 2019))



# Union

"""
Union allows a values to be more than one datatype.
"""
def square(x: Union[int,float]) -> float:
    return x*x

print(square(2.123))  
print(10*"--")
# print(square("i'm a string!!"))    # this will show error.

# Optional
"""
Allows 2 attain 2 values 1-> any specified, 2-> None
"""

def start(name: Optional[str]) -> str:
    if name is None:
        return ("Hi random person!!")
    
    else: 
        return (f"Hi {name}")

print(start('vipin'))
# print(start())

# Any
def random(x: Any):
    return x

print(random(5))
print(random("Ishu"))
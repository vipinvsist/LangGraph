"""
Aim: To use memory in the agent
Use different message types - HumanMessage and AIMessage
Maintain a full conversation history using both message types
Use GPT-4o-mini model using LangChain's ChatOpenAI
Create a sophisticated conversation loop
"""
import os
from pyexpat.errors import messages
from typing import TypedDict, List, Union
from urllib import response
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import START, StateGraph, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

message_count = 0

load_dotenv()

class AgentState(TypedDict):
    # message: List[HumanMessage]
    # messages_ai: List[AIMessage]
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatOpenAI(model="gpt-4o-mini")
def process(state:AgentState)-> AgentState:
    "This function will help in solve the request you input"
    response = llm.invoke(state['messages'])
    state['messages'].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")

    print(f"Current State: {state['messages']}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process_node", process)
graph.add_edge(START,"process_node")
graph.add_edge("process_node",END)
app = graph.compile()

conversation_history=[]
user_input = input("Enter:\n")
while user_input!="exit":
    conversation_history.append(HumanMessage(content=user_input))
    message_count += 1
    # Remove the first message after every 5th message
    if message_count % 5 == 0 and conversation_history:
        conversation_history.pop(0)

    result = app.invoke({"messages": conversation_history})
    # print(result['messages'])
    conversation_history = result['messages']

    user_input = input("Enter:\n")

with open("logging.txt","w") as file:
    file.write("Start of Conversation:\n")
    for messages in conversation_history:
        if isinstance(messages,HumanMessage):
            file.write(f"You: {messages.content}\n")
        elif isinstance(messages, AIMessage):
            file.write(f"AI: {messages.content}\n")
    file.write("END of Conversation")


print("Conversation saved to logging.txt!!")

"""But it consume a lot of tokens. So remove first message after every 5th message """


from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from operator import add as add_messages
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.tools import tool


load_dotenv()

llm = ChatOpenAI(model = "gpt-4o-mini", temperature=0.3)
embeddings = OpenAIEmbeddings(
    model = "text-embedding-3-small"
)

pdf_path = r"C:\Users\Vipin Vashisth\Downloads\Hyperspectral image analysis with Python made easy _ by Antón Garcia _ Abraia _ Feb, 2021 _ Medium _ Abraia.pdf"

if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF file not found: {pdf_path}")

pdf_loader = PyPDFLoader(pdf_path)
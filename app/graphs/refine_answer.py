from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI

class State(TypedDict):
    passage: str
    target_grammar: str
    # generated_insight: str (maybe need, gonna try it without it first)
    generated_question: str

llm = ChatOpenAI(model="gpt-4o")

def get_prompts():
    return {}

def get_graph():
    pass
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

system_prompt = "You are a Latin teacher and you need to generate a " \
"question (in Latin) based on the passage given by the student." \
"The question should only contain Latin words, unless the non-Latin word is found in the passage itself."
"The question should be able to be answered utilizing the {target_grammar} and the content of the passage." \
"The question should not ask for any information that is not in the passage."

class State(TypedDict):
    passage: str
    target_grammar: str
    generated_question: str

llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "Passage:\n\n{passage}")
])
chain = prompt | llm | StrOutputParser()

def get_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("generate_question", generate_question)
    graph_builder.set_entry_point("generate_question")

    return graph_builder.compile()

def generate_question(state: State) -> State:
    return {'generated_question': chain.invoke({
        'passage': state['passage']
    })}
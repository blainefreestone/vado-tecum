from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

system_question_prompt = "You are a Latin expert and you need to generate a question (in Latin) " \
"based on a passage and an insight about the passage given by the user. " \

system_insight_prompt = "You are a Latin expert and you need to generate an insight in Latin based " \
"on the passage given by the user. " \
"The insight should utilize the grammar concept given by the user. " \
"The insight should not contain any information that is not in the passage."

class State(TypedDict):
    passage: str
    target_grammar: str
    generated_insight: str
    generated_question: str

llm = ChatOpenAI()

question_prompt = ChatPromptTemplate.from_messages([
    ("system", system_question_prompt),
    ("user", "Passage:\n\n{passage}\n\nInsight:\n\n{generated_insight}")
])
question_chain = question_prompt | llm | StrOutputParser()

insight_prompt = ChatPromptTemplate.from_messages([
    ("system", system_insight_prompt),
    ("user", "Passage:\n\n{passage}\n\nTarget grammar concept: {target_grammar}")
])
insight_chain = insight_prompt | llm | StrOutputParser()

def get_prompts():
    return {
        'generate_question': question_prompt,
        'generate_insight': insight_prompt
    }

def get_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("generate_question", generate_question)
    graph_builder.add_node("generate_insight", generate_insight)

    graph_builder.set_entry_point("generate_insight")

    graph_builder.add_edge("generate_insight", "generate_question")

    return graph_builder.compile()

def generate_question(state: State) -> State:
    return {'generated_question': question_chain.invoke({
        'passage': state['passage'],
        'generated_insight': state['generated_insight']
    })}

def generate_insight(state: State) -> State:
    return {'generated_insight': insight_chain.invoke({
        'passage': state['passage'],
        'target_grammar': state['target_grammar']
    })}
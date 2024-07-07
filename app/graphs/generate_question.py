from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import yaml

system_question_prompt = "You are a Latin expert and you need to generate a question (in Latin) " \
"based on a passage and an insight about the passage given by the user. " \
"Do not generate any text before or after the question."

system_insight_prompt = "You are a Latin expert and you need to generate an insight (completely in Latin) based " \
"on the passage given by the user. " \
"The insight should utilize the grammar concept given by the user. " \
"The insight should not contain any information that is not in the passage. " \
"The insight should be a complete sentence. " \
"Do not generate any text before or after the insight."

class State(TypedDict):
    passage: str
    target_grammar: str
    generated_insight: str
    generated_question: str

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
    llm_provider = config['llm_provider']
    openai_api_key = config['openai_api_key']
    openai_model = config['openai_model']
    anthropic_api_key = config['anthropic_api_key']
    anthropic_model = config['anthropic_model']

if llm_provider == "openai":
    llm = ChatOpenAI(model_name=openai_model, api_key=openai_api_key)
elif llm_provider == "anthropic":
    llm = ChatAnthropic(model_name=anthropic_model, api_key=anthropic_api_key)
else:
    raise ValueError("Invalid LLM provider in config.yaml")

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
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal
import yaml

system_grade_prompt = "You are a Latin expert and you need to grade a student's answer to a question. " \
"The question is based on a passage and intends to test the student's understanding of it and ability to utilize the target grammar concept. " \
"Question: {generated_question}\n\n" \
"Passage: {passage}\n\n" \

system_refine_prompt = "You are a Latin teacher and you need to help a student improve their answer to the following question: " \
"{generated_question} \n" \
"The student's answer is not completely relevant to the question because: {comment}. " \
"Always respond in Latin. " \
"Only respond with the feedback, do not rewrite the answer for the student, that is their responsibility. " \

class Relevance(BaseModel):
    relevant: bool = Field(..., description="Does the answer attempt to answer the question?")
    comment: str = Field(..., description="One sentence explaining the grade given.")

class State(TypedDict):
    passage: str
    target_grammar: str
    generated_question: str
    answer: str
    relevant: Relevance
    comment: str

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

structured_llm = llm.with_structured_output(Relevance)

grade_prompt = ChatPromptTemplate.from_messages([
    ("system", system_grade_prompt),
    ("user", "Answer:\n\n{answer}")
])

grade_chain = grade_prompt | structured_llm

refine_prompt = ChatPromptTemplate.from_messages([
    ("system", system_refine_prompt),
    ("user", "Answer:\n\n{answer}")
])

refine_chain = refine_prompt | llm | StrOutputParser()

def get_prompts():
    return {
        'grade': grade_prompt,
        'refine': refine_prompt
    }

def get_graph():
    graph_builder = StateGraph(State)

    graph_builder.add_node("grade_answer", grade_answer)
    graph_builder.add_node("refine_relevance", refine_relevance)

    graph_builder.set_entry_point("grade_answer")

    graph_builder.add_conditional_edges(
        "grade_answer",
        router
    )

    return graph_builder.compile()

def grade_answer(state: State) -> State:
    return {
        'relevant': grade_chain.invoke({
            'generated_question': state['generated_question'],
            'passage': state['passage'],
            'answer': state['answer'],
        })
    }

def router(state: State) -> Literal[
    "refine_relevance",
    "__end__"
    ]:
    grade = state['relevant']
    
    if grade.relevant:
        return "__end__"
    else:
        return "refine_relevance"

def refine_relevance(state: State) -> State:
    return {"comment": refine_chain.invoke({
        "answer": state["answer"],
        "generated_question": state["generated_question"],
        "comment": state["relevant"].comment,
    })}
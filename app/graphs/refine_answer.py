from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal

system_grade_prompt = "You are a Latin expert and you need to grade a student's answer to a question. " \
"The question is based on a passage and intends to test the student's understanding of the following passage and ability to utilize the target grammar concept. " \
"Question: {generated_question}\n\n" \
"Passage: {passage}\n\n" \
"Target grammar concept: {target_grammar}\n\n"

system_laud_answer_prompt = "You are a helpful Latin teacher and you need to provide feedback to a student. " \
"Question: {generated_question}\n\n" \
"Passage: {passage}\n\n" \
"Target grammar concept: {target_grammar}\n\n" \
"The student will give you a good answer. "
"Laud the student's answer and ability, and provide constructive feedback (all in Latin). " \

class AnswerGrade(BaseModel):
    correctness: float = Field(..., ge=0, le=1, description="How correct is the information in the answer based on the passage?")
    relevance: float = Field(..., ge=0, le=1, description="How relevant is the response to the question asked?")
    use_of_grammar_target: float = Field(..., ge=0, le=1, description="Does the answer try to use the target grammar concept?")
    correct_use_of_grammar_target: Optional[float] = Field(None, ge=0, le=1, description="Does the answer correctly use the target grammar concept? Should be None if the answer does not try to use the target grammar concept.")
    fluency: float = Field(..., ge=0, le=1, description="How well-written is the answer? Does it make sense? Is it grammatically correct?")

class State(TypedDict):
    passage: str
    target_grammar: str
    generated_question: str
    answer: str
    # messages: Annotated[list, add_messages]
    grade: AnswerGrade

llm = ChatOpenAI(model="gpt-4o")
structured_llm = llm.with_structured_output(AnswerGrade)

grade_prompt = ChatPromptTemplate.from_messages([
    ("system", system_grade_prompt),
    ("user", "Answer:\n\n{answer}")
])

grade_chain = grade_prompt | structured_llm

laud_answer_prompt = ChatPromptTemplate.from_messages([
    ("system", system_laud_answer_prompt),
    ("user", "Answer:\n\n{answer}")
])

laud_answer_chain = laud_answer_prompt | llm | StrOutputParser()

def get_prompts():
    return {
        'grade': grade_prompt
    }

def get_graph():
    graph_builder = StateGraph(State)

    graph_builder.add_node("grade_answer", grade_answer)
    graph_builder.add_node("laud_answer", laud_answer)
    graph_builder.add_node("refine_correctness", refine_correctness)
    graph_builder.add_node("refine_relevance", refine_relevance)
    graph_builder.add_node("refine_use_of_grammar_target", refine_use_of_grammar_target)
    graph_builder.add_node("refine_correct_use_of_grammar_target", refine_correct_use_of_grammar_target)
    graph_builder.add_node("refine_fluency", refine_fluency)

    graph_builder.set_entry_point("grade_answer")

    graph_builder.add_conditional_edges(
        "grade_answer",
        refine_router
    )

    return graph_builder.compile()

def grade_answer(state: State) -> State:
    return {
        'grade': grade_chain.invoke({
            'generated_question': state['generated_question'],
            'passage': state['passage'],
            'answer': state['answer'],
            'target_grammar': state['target_grammar']
        })
    }

def refine_router(state: State) -> Literal[
    "refine_correctness", 
    "refine_relevance", 
    "refine_use_of_grammar_target", 
    "refine_correct_use_of_grammar_target", 
    "refine_fluency",
    "laud_answer"
    ]:
    grade = state['grade']
    
    # find the lowest score
    lowest_score = min(
        grade for grade in [
            grade.correctness, 
            grade.relevance, 
            grade.use_of_grammar_target, 
            grade.correct_use_of_grammar_target, 
            grade.fluency
        ] if grade is not None
    )
    # if the lowest score is greater than 0.7, the answer is good enough
    if lowest_score >= 0.7:
        return "laud_answer"
    
    if lowest_score == grade.correctness:
        return "refine_correctness"
    elif lowest_score == grade.relevance:
        return "refine_relevance"
    elif lowest_score == grade.use_of_grammar_target:
        return "refine_use_of_grammar_target"
    elif lowest_score == grade.correct_use_of_grammar_target:
        return "refine_correct_use_of_grammar_target"
    elif lowest_score == grade.fluency:
        return "refine_fluency"
    
def laud_answer(state: State) -> State:
    return {"comment": laud_answer_chain.invoke({
        "answer": state["answer"],
        "generated_question": state["generated_question"],
        "passage": state["passage"],
        "target_grammar": state["target_grammar"]
    })}

def refine_correctness(state: State) -> State:
    return state

def refine_relevance(state: State) -> State:
    return state

def refine_use_of_grammar_target(state: State) -> State:
    return state

def refine_correct_use_of_grammar_target(state: State) -> State:
    return state

def refine_fluency(state: State) -> State:
    return state
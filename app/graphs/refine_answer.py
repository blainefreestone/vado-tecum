from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field

system_grade_prompt = "You are a Latin expert and you need to grade a student's answer to a question. " \
"The question is based on a passage and intends to test the student's understanding of the following passage and ability to utilize the target grammar concept. " \
"Question: {generated_question}\n\n" \
"Passage: {passage}\n\n" \
"Target grammar concept: {target_grammar}\n\n" \

class AnswerGrade(BaseModel):
    correctness: float = Field(..., ge=0, le=1, description="How correct is the information in the answer based on the passage?")
    relevance: float = Field(..., ge=0, le=1, description="How relevant is the response to the question asked?")
    use_of_grammar_target: float = Field(..., ge=0, le=1, description="Does the answer try to use the target grammar concept?")
    correct_use_of_grammar_target: Optional[float] = Field(None, ge=0, le=1, description="Does the answer correctly use the target grammar concept? Should be None if the answer does not try to use the target grammar concept.")

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

def get_prompts():
    return {
        'grade': grade_prompt
    }

def get_graph():
    graph_builder = StateGraph(State)

    graph_builder.add_node("grade_answer", grade_answer)

    graph_builder.set_entry_point("grade_answer")

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
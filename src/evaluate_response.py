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
from langchain_core.messages import SystemMessage
from typing import Literal
import yaml

class AnswerGrade(BaseModel):
    correctness: float = Field(..., ge=0, le=1, description="How correct is the information in the answer based on the passage?")
    fluency: float = Field(..., ge=0, le=1, description="How well-written is the answer? Does it make sense? Is it grammatically correct?")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = llm.with_structured_output(AnswerGrade)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a Latin expert and you need to grade a student's answer to a question. " \
                "The question is based on a passage and intends to test the student's understanding of the following passage. " \
                "Passage: {passage}\n\n" \
                "Question: {generated_question}\n\n" \
            )
        )
    ]
)

chain = prompt | structured_llm 
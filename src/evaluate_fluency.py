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
from langchain_core.prompts import HumanMessagePromptTemplate

class Fluency(BaseModel):
    fluent: bool = Field(..., description="Is the student's answer in Latin AND well-written AND grammatically and syntactically correct.")
    explanation: str = Field(..., description="A one sentence explanation if the student's answer is not fluent.")
    concepts: list[str] = Field(..., description="A list of the specific grammar concept(s) the student should review in as few words as possible.")

llm = ChatOpenAI(model="gpt-4o", temperature=0)
structured_llm = llm.with_structured_output(Fluency)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a Latin expert. " \
                "Question: {generated_question}\n\n" \
            )
        ),
        HumanMessagePromptTemplate.from_template("Answer: {input}"),
    ]
)

chain = prompt | structured_llm 

### Rough test cases

print(chain.invoke({
    "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'",
    "generated_question": "Quid facere debebant cives ut indulgentiam domini Imperatoris promerentur?",
    "input": "Cives ad bonam mentem redire debent."
}))

# print(chain.invoke({
#     "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'",
#     "generated_question": "Quid facere debebant cives ut indulgentiam domini Imperatoris promerentur?",
#     "input": "Cives ad Carthaginem ire debebant."
# }))

# print(chain.invoke({
#     "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'",
#     "generated_question": "Quid facere debebant cives ut indulgentiam domini Imperatoris promerentur?",
#     "input": "They needed to go to Carthage."
# }))

# print(chain.invoke({
#     "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'",
#     "generated_question": "Quid facere debebant cives ut indulgentiam domini Imperatoris promerantur?",
#     "input": "Cives ad bonam mentem redire debet."
# }))
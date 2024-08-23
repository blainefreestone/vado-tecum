from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate
class Correctness(BaseModel):
    correct: bool = Field(..., description="Is the user's response to the following question a correct answer to the question based on the given passage?")
    correct_answer: str = Field(..., description="A one sentence answer, in Latin, that would be correct.")
    explanation: str = Field(..., description="A one sentence explanation if the student's answer is not correct.")

llm = ChatOpenAI(model="gpt-4o", temperature=0)
structured_llm = llm.with_structured_output(Correctness)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are a Latin expert. " \
            "Passage: {passage}\n\n" \
            "Question: {question}\n\n" \
        ),
        HumanMessagePromptTemplate.from_template("Answer: {input}"),
    ]
)

chain = prompt | structured_llm 

### Rough test cases

# print(chain.invoke({
#     "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'",
#     "question": "Quomodo cives indulgentiam domini Imperatoris promeri possunt?",
#     "input": "Cives ad bonam mentem redire debent ut indulgentiam domini Imperatoris promerentur."
# }))

# print(chain.invoke({
#     "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'",
#     "question": "Quid facere debebant cives ut indulgentiam domini Imperatoris promerentur?",
#     "input": "Cives ad bonam mentem redire debent."
# }))

# print(chain.invoke({
#     "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'",
#     "question": "Quid facere debebant cives ut indulgentiam domini Imperatoris promerentur?",
#     "input": "Cives ad Carthaginem ire debebant."
# }))

# print(chain.invoke({
#     "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'",
#     "question": "Quid facere debebant cives ut indulgentiam domini Imperatoris promerentur?",
#     "input": "They needed to go to Carthage."
# }))

# print(chain.invoke({
#     "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'",
#     "question": "Quid facere debebant cives ut indulgentiam domini Imperatoris promerantur?",
#     "input": "Cives ad bonam mentem redire debet."
# }))
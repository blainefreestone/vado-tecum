from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables import Runnable

class Correctness(BaseModel):
    correct: bool = Field(..., description="Does the students answer correctly respond to the question based on the information given in the passage?")
    explanation: str = Field(..., description="A one sentence explanation explaining how the student can improve their response if the answer is incorrect.")

llm = ChatOpenAI(model="gpt-4o", temperature=0)
structured_llm = llm.with_structured_output(Correctness)

correct_answer_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a Latin expert. You are to generate the correct response to the question provided by the user based on the given passage. " \
                "Passage: {passage}\n\n" \
            )
        ),
        HumanMessagePromptTemplate.from_template("Question: {question}"),
    ]
)

correct_answer_chain = correct_answer_prompt | llm | StrOutputParser()

evaluation_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a Latin expert. " \
                "You are to evaluate the correctness of the student's response to the question based on the given passage. " \
                "Passage: {passage}\n\n" \
                "Question: {question}\n\n" \
                "Correct Answer: {correct_answer}\n\n" \
            )
        ),
        HumanMessagePromptTemplate.from_template("Answer: {input}"),
    ]
)

evaluation_chain = evaluation_prompt | structured_llm 

def evaluate_correctness(info):
    correct_answer = correct_answer_chain.invoke({
        "passage": info["passage"],
        "question": info["generated_question"]
    })

    print(correct_answer)

    evaluation = evaluation_chain.invoke({
        "passage": info["passage"],
        "question": info["generated_question"],
        "correct_answer": correct_answer,
        "input": info["input"]
    })

    return evaluation

### Rough test cases

print(evaluate_correctness({
    "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'",
    "generated_question": "Quid facere debebant cives ut indulgentiam domini Imperatoris promerentur?",
    "input": "Cives ad bonam mentem redire debent ut indulgentiam domini Imperatoris promerentur."
}))

# print(chain.invoke({
#     "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'",
#     "generated_question": "Quid facere debebant cives ut indulgentiam domini Imperatoris promerentur?",
#     "input": "Cives ad bonam mentem redire debent."
# }))

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
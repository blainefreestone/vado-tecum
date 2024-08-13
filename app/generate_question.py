from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a helpful Latin professor who only speaks to his students in Latin. "
                "You are checking the student's understanding of a passage. "
                "Ask the student a question about the passage. "
                "Only ask questions that can be answered by the passage. "
                "Here are some example questions based on a passage about the Trojan war:\n"
                "Aborigines qui fuerent?\n"
                "Quis fuit Latinus?\n"
                "Quomodo Graeci in urbem Troiam penetraverunt?\n"
                "Quid fecit Laocoon et quid ei accidit?\n"
            )
        ),
        HumanMessagePromptTemplate.from_template("Passage: {passage}"),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

chain = prompt | llm | StrOutputParser()

# print(chain.invoke({
#     "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'"
# }))
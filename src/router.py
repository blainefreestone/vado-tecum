from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import  ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "Given the conversation below, choose the next worker to continue the conversation."
                " Choose from the following workers:\n"
                "explain_word_or_phrase - Explain the meaning of a word or phrase if the student asks.\n"
                "generate_question - Generate a question to test the students understanding when the indicate they are ready.\n"
                " Do not respond with more than one word."
            )
        ),
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)

chain = (
    prompt
    | ChatOpenAI(model="gpt-4o-mini", temperature=0)
    | StrOutputParser()
)

### Rough test cases

# print(chain.invoke({
#     "messages": [
#         "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.' nterroga me de significatione verborum vel locutionum, aut auxilium in intellegendo locum quaere. Cum paratus eris, responde 'paratus sum'.", 
#         "Quid significat 'consulibus'?"
#     ]
# }))

# print(chain.invoke({
#     "messages": [
#         "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.' nterroga me de significatione verborum vel locutionum, aut auxilium in intellegendo locum quaere. Cum paratus eris, responde 'paratus sum'.", 
#         "paratus sum"
#     ]
# }))

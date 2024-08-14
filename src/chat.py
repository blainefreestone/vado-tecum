from router import chain as router_chain
from generate_question import chain as generate_question_chain
from explain_word_or_phrase import agent_executor as explain_word_or_phrase_agent_executor
from langchain_core.runnables import RunnableLambda

def route(info):
    if info["worker"] == "generate_question":
        return generate_question_chain.invoke({
            "passage": info["passage"]
        })
    elif info["worker"] == "explain_word_or_phrase":
        return explain_word_or_phrase_agent_executor.invoke({
            "passage": info["passage"],
            "input": info["input"]
        })["output"]
    else:
        return

full_chain = {"worker": router_chain, "input": lambda x: x["input"], "messages": lambda x: x["messages"], "passage": lambda x: x["passage"]} | RunnableLambda(route)

### Rough test cases

# user_input = "Quid significat 'consulibus'?"
# user_input = "paratus sum"

# print(full_chain.invoke({
#     "messages": [
#         "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.' nterroga me de significatione verborum vel locutionum, aut auxilium in intellegendo locum quaere. Cum paratus eris, responde 'paratus sum'.", 
#     ],
#     "input": user_input,
#     "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'",
# }))
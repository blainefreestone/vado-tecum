from router import chain as router_chain
from generate_question import chain as generate_question_chain
from explain_word_or_phrase import agent_executor as explain_word_or_phrase_agent_executor
from evaluate_correctness import chain as evaluate_correctness_chain
from evaluate_fluency import chain as evaluate_fluency_chain
from langchain_core.runnables import RunnableLambda

def route(info):
    if info["worker"] == "generate_question":
        question =  generate_question_chain.invoke({
            "passage": info["passage"]
        })
        return {
            "question": question,
            "response": question
        }
    elif info["worker"] == "explain_word_or_phrase":
        explanation = explain_word_or_phrase_agent_executor.invoke({
            "passage": info["passage"],
            "input": info["input"]
        })["output"]
        return {
            "response": explanation
        }
    elif info["worker"] == "evaluate_response":
        correctness = evaluate_correctness_chain.invoke({
            "passage": info["passage"],
            "question": info["question"],
            "input": info["input"]
        })

        if correctness.correct is True:
            fluency = evaluate_fluency_chain.invoke({
                "question": info["question"],
                "input": info["input"]
            })

            if fluency.fluent is True:
                return {
                    "response": "Recte respondisti!"
                }
            else:
                return {
                    "response": fluency.explanation
                }
        else:
            return {
                "response": correctness.explanation
            }
    else:
        return

full_chain = {"worker": router_chain, "input": lambda x: x.get("input"), "messages": lambda x: x.get("messages"), "passage": lambda x: x.get("passage"), "question": lambda x: x.get("question")} | RunnableLambda(route)

### Rough test cases

# user_input = "Quid significat 'consulibus'?"
# user_input = "paratus sum"
# # user_input = "Cives ad bonam mentem redire debent ut indulgentiam domini Imperatoris promerentur."
# user_input = "Cives ad Carthaginem ire debebant."
# user_input = "They need to return to a sound mind."

# print(full_chain.invoke({
#     "messages": [
#         "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.' nterroga me de significatione verborum vel locutionum, aut auxilium in intellegendo locum quaere. Cum paratus eris, responde 'paratus sum'.", 
#     ],
#     "input": user_input,
#     "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'",
# }))

# print(full_chain.invoke({
#     "messages": [
#         "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.' nterroga me de significatione verborum vel locutionum, aut auxilium in intellegendo locum quaere. Cum paratus eris, responde 'paratus sum'.", 
#         "Paratus sum",
#         "Quid facere debebant cives ut indulgentiam domini Imperatoris promerentur?",
#     ],
#     "input": user_input,
#     "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'",
#     "question": "Quid facere debebant cives ut indulgentiam domini Imperatoris promerentur?",
# }))
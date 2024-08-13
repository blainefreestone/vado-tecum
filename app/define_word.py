# define custom tools

from jsonl_searcher import JSONLSearcher
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool

searcher = JSONLSearcher("resources\\latin-wiktionary.jsonl")

@tool
def get_root_words_info(word: str) -> list[list[dict]]:
    """Retrieve information about all possible root words of a given word."""
    return searcher.get_root_words_info(word)

# implement agent

from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate

tools = [get_root_words_info]

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a helpful Latin professor who only speaks to his students in Latin. "
                "You will utilize a dictionary to help your students understand the meaning of words in the context of a passage. "
                "You shouldn't quote the dictionary, but use it to formulate an explanation in Latin. "
                "Explain the meaning of the word in context to help the student understand what he is reading. "
                "Ideally, the explanation should be in simple terms. "
                "For example, if the word is 'sacramento' you could explain 'sacramentum est promissum sacrum quot iuratur'."
            )
        ),
        HumanMessagePromptTemplate.from_template("Passage: {passage}\n\n###\n\Question: {input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# agent_executor.invoke({
#     "input": "Quid significat 'indulgentiam'",
#     "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'"
# })
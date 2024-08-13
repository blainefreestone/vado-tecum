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
                "You are helping a student understand a word or phrase in a passage. "
                "If the student asks you what a word means, you should explain the meaning of the word utilizing a dictionary. "
                "You shouldn't quote the dictionary, but use it to formulate an explanation in Latin. "
                "If the student asks you what a phrase means, you should explain the meaning of the phrase. "
                "Ideally, the explanation should be in simple terms and in the context of the passage. "
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

agent_executor.invoke({
    "input": "Quid significat 'ad bonam mentem redeatis'?",
    "passage": "Praesente (bis) et Claudiano consulibus, sexto decimo kalendas Augustas, Carthagine in secretario impositis, Sperato, Nartzalo ... Saturninus proconsul dixit: 'Potestis indulgentiam domini nostri Imperatoris promereri, si ad bonam mentem redeatis.'"
})
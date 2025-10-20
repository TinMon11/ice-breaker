import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor

# Ensure project root is on sys.path so local imports work when running this file directly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.tools import get_profile_url
from langchain import hub

load_dotenv()

def lookup(name: str) -> str:
    """
    Lookup a person's Twitter profile URL
    Args:
        name: The name of the person
    Returns:
        The Twitter profile URL or an error message
    """

    llm_model = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

    template = """
    Given the full name of {name_of_person} I want you to get the link to his Twitter profile.
    Your answer should only contain the username of the Twitter profile.
    Call the function get_profile_url with the name of the person and the platform "twitter" to get the Twitter profile URL.
    Example: @elonmusk
    """

    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=template
    )

    def get_twitter_profile(name_of_person: str) -> str:
        return get_profile_url(name_of_person, "twitter")

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 Twitter profile",
            func=get_twitter_profile,
            description="Useful for any time you need to find someone's Twitter profile URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm_model, tools=tools_for_agent, prompt=react_prompt
    )

    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True
    )

    result = agent_executor.invoke({"input": prompt_template.invoke({"name_of_person": name})})
    
    return result["output"]
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
    Lookup a person's LinkedIn profile URL
    Args:
        name: The name of the person
    Returns:
        The LinkedIn profile URL or an error message
    """

    llm_model = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

    template = """
    Given the full name of {name_of_person} I want you to get their LinkedIn profile URL.
    Your answer should only contain a URL.
    Example: https://www.linkedin.com/in/john-doe-1234567890/
    """

    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=template
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile",
            func=get_profile_url,
            description="Useful for any time you need to find someone's LinkedIn profile URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm_model, tools=tools_for_agent, prompt=react_prompt
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke({"input": prompt_template.invoke({"name_of_person": name})})
    
    return result["output"]
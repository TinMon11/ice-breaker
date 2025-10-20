from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from thrid_parties import linkedin_lookup_agent
from thrid_parties.linkedin import scrape_linkedin_profile

load_dotenv()


def ice_breaker_with(name: str) -> str:
    linkedin_user_name = linkedin_lookup_agent.lookup(name)
    linkedin_profile_data = scrape_linkedin_profile(linkedin_user_name)

    summary_template = """
    Given the information {information} about a person, I want you to create:
    - A short summary
    - Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

    chain = summary_prompt_template | llm

    linkedin_profile_data = scrape_linkedin_profile("eden_marko")

    result = chain.invoke({"information": linkedin_profile_data})

    print(result.content)


if __name__ == "__main__":
    print(ice_breaker_with("Eden Marco"))

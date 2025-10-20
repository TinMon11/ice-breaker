from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

def get_profile_url(name_of_person: str) -> str:
    """
    Search the web for information
    Args:
        query: The name of the person to search for
    Returns:
        The LinkedIn profile URL of the person or an error message
    """
    search = TavilySearch()
    query = (
        f"Search the web in order to get the LinkedIn profile URL of {name_of_person}"
    )
    results = search.run(query)
    return results["results"][0]["url"]

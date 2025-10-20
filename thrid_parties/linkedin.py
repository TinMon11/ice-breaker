import os
import requests
from dotenv import load_dotenv

load_dotenv()


linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json"


def scrape_linkedin_profile(user_name: str):
    """
    Scrapes information from LinkedIn profiles
    Manually scrape the information from the LinkedIn profile
    Args:
        user_name: The username of the LinkedIn profile
    Returns:
        A dictionary containing the scraped information
    """

    response = requests.get(linkedin_profile_url, timeout=10)
    if response.status_code != 200:
        raise Exception(
            f"Failed to scrape LinkedIn profile. Status code: {response.status_code}"
        )

    data = response.json()

    # Remove emtpy fields from the response
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None) and k not in ["certifications"]
    }

    return data


if __name__ == "__main__":
    print(scrape_linkedin_profile(linkedin_profile_url))

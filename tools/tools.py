from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import requests
import os

load_dotenv()


def get_profile_url(name_of_person: str, platform: str) -> str:
    """
    Search the web for information
    Args:
        name_of_person: The name of the person to search for
        platform: The platform to search for (linkedin or twitter)
    Returns:
        The {platform} profile URL of the person or an error message
    """
    search = TavilySearch()
    query = (
        f"""Search the {platform} profile URL of {name_of_person}.
        Do not include any other text in your response. And do not search how to get that profiles.
        Your query should be pretty straight forward and to the point
        Example:
        "Linedin profile John Doe"
        "Twitter profile John Doe"
        """
    )
    results = search.run(query)
    print("RESULTS: ", results)
    print("Type of results: ", type(results))
    if not isinstance(results, dict) or "results" not in results:
        return "No results found"

    items = results.get("results", []) or []
    urls = [item.get("url", "") for item in items if isinstance(item, dict)]

    if platform == "linkedin":
        for url in urls:
            if "linkedin.com/in" in url:
                return url
        return urls[0] if urls else "No LinkedIn profile found"
    elif platform == "twitter":
        banned_first_segments = {
            "home", "i", "share", "intent", "notifications", "messages", "explore",
            "search", "hashtag", "topics", "settings", "compose", "login", "signup",
            "tos", "privacy"
        }
        for url in urls:
            if "twitter.com/" in url or "x.com/" in url:
                clean = url.split("?")[0].split("#")[0]
                parts = [p for p in clean.split("/") if p]
                # Expect formats like: https://x.com/<handle>[/status/...]
                if len(parts) >= 2:  # has domain and at least one path seg
                    handle = parts[1]
                    if handle and handle.lower() not in banned_first_segments:
                        return handle if handle.startswith("@") else f"@{handle}"
        return "No Twitter profile found"
    else:
        return "Invalid platform"


def get_recent_twitter_posts(username: str, amount: int = 10):
    """Get the 10 most recent tweets by specified user.

    # Parameters:
        username (str): Username of the user to search for their most recent tweets.
        amount (int): Number of tweets to return. Defaults to 10 if not specified.

    Raises:
        Exception: If 429, Twitter/X API Rate limit is reached.
        Exception: Other than 200 or 429 for internal server errors.

    # Returns:
        Union[str, list[dict]]: "Successful" if direct_render=True, otherwise list of tweets.
    """
    if not username:
        return "Please provide a valid username."

    cleaned_username = username.lstrip("@")

    query_params = f"query=from:{cleaned_username}&tweet.fields=created_at&expansions=author_id&user.fields=created_at"
    if amount > 10 and amount <= 20:
        query_params += f"&max_results={amount}"

    BASE_URL = "https://api.x.com/2"
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

    response = requests.get(
        f"{BASE_URL}/tweets/search/recent?{query_params}",
        headers={"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"},
    )

    if response.status_code == 429:
        raise Exception("X API rate limit exceeded.")
    elif response.status_code != 200:
        raise Exception(f"X API error: {response.text}")

    tweets = response.json().get("data", [])
    for tweet in tweets:
        tweet["username"] = cleaned_username

    if amount < 10:
        tweets = tweets[:amount]

    return tweets


if __name__ == "__main__":
    print(get_recent_twitter_posts("elonmusk", 10))

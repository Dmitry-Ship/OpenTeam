from typing import Annotated
from dotenv import load_dotenv
from tavily import TavilyClient
import os

load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def ask_context(question: Annotated[str, "Additional question to specify context"]) -> Annotated[str, "Additional context"]:
    """
    Ask for additional context
    """
    additional_query = input("❓ " + question + ": ")
    return search_internet(additional_query)

def search_internet(query: Annotated[str, "The query to search for"]) -> Annotated[str, "The answer to the query"]:
    """
    Search the internet
    """
    print("🔍 searching ...")
    response = tavily.search(query=query, search_depth="advanced", include_images=True, include_answer=True)
    context = [{"url": obj["url"], "content": obj["content"]} for obj in response['results']]

    return context


    


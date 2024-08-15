from dotenv import load_dotenv
from tavily import TavilyClient
import openai
from pydantic import BaseModel
import os

load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

class AskContext(BaseModel):
    question: str

ask_context_params = openai.pydantic_function_tool(AskContext, name="ask_context", description="Ask context")
def ask_context(question):
    additional_query = input("❓ " + question + ": ")
    return search_internet(additional_query)


class Search(BaseModel):
    query: str
    
search_internet_params = openai.pydantic_function_tool(Search, name="search", description="Search the internet")
def search_internet(query):
    print("🔍 searching ...", query)
    response = tavily.search(query=query, search_depth="advanced", include_images=True, include_answer=True)
    context = [{"url": obj["url"], "content": obj["content"]} for obj in response['results']]

    return context


    


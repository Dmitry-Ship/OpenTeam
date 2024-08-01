from .tools import search_internet, ask_context
from base import Agent
from dotenv import load_dotenv
import os

load_dotenv(override=True)

MODEL = os.getenv("OPENAI_MODEL_NAME")

search_query_suggester = Agent(
    name="search_query_suggester", 
    model=MODEL,
    system_message="""
    Based on the provided information, suggest three followup search queries that progressivly delve deeper into the subject. 
    Respond in JSON and nothing else:
    {
        "related": ["query_1", "query_2", "query_3"]
    }
""",
)

searcher = Agent(
    name="searcher", 
    model=MODEL,
    system_message="""
    As a professional search expert, you possess the ability to search for any information on the web. 
    For each user query, utilize the search results to their fullest potential to provide additional information and assistance in your response.
    Aim to directly address the user's question, augmenting your response with insights gleaned from the search results.
    Whenever quoting or referencing information from a specific URL, always cite the source URL explicitly. Please match the language of the response to the user's language.
    Always answer in Markdown format. Links and images must follow the correct format.
    Link format: [link text](url)
    Image format: ![alt text](url)
    Please match the language of the response to the user's language.

    If it is necessary, use ask_context to get additional context, otherwise call search_internet.
""",
    tools=[search_internet, ask_context],
)






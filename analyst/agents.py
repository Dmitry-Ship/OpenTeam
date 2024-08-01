from base import Agent
from .tools import run_query, get_schema
from dotenv import load_dotenv
import os

load_dotenv(override=True)

MODEL = os.getenv("OPENAI_MODEL_NAME")

analyst = Agent(
    name="analyst", 
    model=MODEL,
    system_message=f"""
    You are an analyst. Your goal is to solve a given by retrieving data from the database.
    Here is the schema of the database:
    {get_schema()}

    Use run_query to retrieve data from the database. 
    If you are asked to visualize the data, write python code (in a python coding block) that will create a graph visualization of provided data.
    Write 'TERMINATE' if the task is done""",
    tools=[run_query],
)







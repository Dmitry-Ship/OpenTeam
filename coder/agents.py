
from dotenv import load_dotenv
from .tools import see_file, list_dir, create_file_with_code, modify_code
from base import Agent

load_dotenv(override=True)

engeneer = Agent(
    name="Engineer",
    model="gpt-3.5-turbo",
    system_message="""
    I'm Engineer. I'm expert in python programming. I'm executing code tasks required by Admin.
    """,
    tools=[see_file, list_dir, create_file_with_code, modify_code],
)

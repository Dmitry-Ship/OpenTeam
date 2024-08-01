
from dotenv import load_dotenv
from .tools import see_file, list_dir, create_file_with_code, modify_code, get_files_content
from base import Agent

load_dotenv(override=True)

engeneer = Agent(
    name="Engineer",
    model="gpt-4o-mini",
    system_message="""
    I'm Engineer. I'm expert in python programming. I'm executing code tasks required by Admin.
    """,
    tools=[get_files_content, see_file, list_dir, create_file_with_code, modify_code],
)

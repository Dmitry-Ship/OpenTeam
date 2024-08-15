
from dotenv import load_dotenv
from .tools import see_file, list_dir, create_file_with_code, modify_code, get_files_content, get_files_content_params, create_file_params, modify_code_params, list_dir_params, see_file_params
from base import Agent

load_dotenv(override=True)

engeneer = Agent(
    name="Engineer",
    model="gpt-4o-mini",
    system_message="""
    I'm Engineer. I'm expert in python programming. I'm executing code tasks required by Admin.
    """,
    tools_mapper={"get_files_content": get_files_content, "see_file": see_file, "list_dir": list_dir, "create_file_with_code": create_file_with_code, "modify_code": modify_code},
    tools_params=[get_files_content_params, create_file_params, modify_code_params, list_dir_params, see_file_params],
)

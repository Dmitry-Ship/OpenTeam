from typing import Annotated
import os
import openai
from pydantic import BaseModel

default_path = current_dir = os.getcwd() + "/"

class GetFilesContent(BaseModel):
    directory: Annotated[str, "Directory to check."]

get_files_content_params = openai.pydantic_function_tool(GetFilesContent, name="get_files_content", description="Get content of all the files in the directory")
def get_files_content(directory: Annotated[str, "Directory to check."]) -> Annotated[str, "Content of all the files in the directory"]:
    result = []
    
    def is_hidden(filepath):
        for part in filepath.split(os.sep):
            if part.startswith('.'):
                return True
        return False

    print("🔎 Searching for files ...", default_path + directory)
    for root, dirs, files in os.walk(default_path):
        # Exclude hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.py') and not is_hidden(os.path.join(root, file)):
                file_path = os.path.join(root, file)
                result.append(f"File: {file_path}")
                with open(file_path, 'r') as f:
                    result.append(f.read())
    print("✅ Done", result)
    return "\n".join(result)


class ListDir(BaseModel):
    directory: Annotated[str, "Directory to check."]

list_dir_params = openai.pydantic_function_tool(ListDir, name="list_dir", description="List all the files in the directory")
def list_dir(directory: Annotated[str, "Directory to check."]) -> Annotated[list[str], "List of files in the directory"]:
    files = os.listdir(directory)
    return 0, files

class SeeFile(BaseModel):
    filename: Annotated[str, "Name and path of file to check."]

see_file_params = openai.pydantic_function_tool(SeeFile, name="see_file", description="See the contents of the file")
def see_file(filename: Annotated[str, "Name and path of file to check."]) -> Annotated[str, "File contents"]:
    with open(default_path + filename, "r") as file:
        lines = file.readlines()
    formatted_lines = [f"{i+1}:{line}" for i, line in enumerate(lines)]
    file_contents = "".join(formatted_lines)

    return 0, file_contents

class ModifyCode(BaseModel):
    filename: Annotated[str, "Name and path of file to change."]
    start_line: Annotated[int, "Start line number to replace with new code."]
    end_line: Annotated[int, "End line number to replace with new code."]
    new_code: Annotated[str, "New piece of code to replace old code with. Remember about providing indents."]

modify_code_params = openai.pydantic_function_tool(ModifyCode, name="modify_code", description="Modify the code in the file")
def modify_code(
    filename: Annotated[str, "Name and path of file to change."],
    start_line: Annotated[int, "Start line number to replace with new code."],
    end_line: Annotated[int, "End line number to replace with new code."],
    new_code: Annotated[str, "New piece of code to replace old code with. Remember about providing indents."],
) -> Annotated[tuple[int, str], "Status code and message"]:
    with open(filename, "r+") as file:
        file_contents = file.readlines()
        file_contents[start_line - 1 : end_line] = [new_code + "\n"]
        file.seek(0)
        file.truncate()
        file.write("".join(file_contents))
    return 0, "Code modified"

class CreateFile(BaseModel):
    filename: Annotated[str, "Name and path of file to create."]

create_file_params = openai.pydantic_function_tool(CreateFile, name="create_file", description="Create a new file")

def create_file_with_code(
    filename: Annotated[str, "Name and path of file to create."], code: Annotated[str, "Code to write in the file."]
) -> Annotated[tuple[int, str], "Status code and message"]:
    with open(filename, "w") as file:
        file.write(code)
    return 0, "File created successfully"
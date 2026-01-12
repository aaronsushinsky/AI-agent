import os
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        content = ""
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))      
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir == False:
            return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

        if os.path.isfile(target_dir) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000
        with open(target_dir, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
      
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns a string from a regular file in the permitted working directory, limited to 10,000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="A string representing the relative path of the file.",
                ),
            },
        required=["file_path"]
        ),
    )
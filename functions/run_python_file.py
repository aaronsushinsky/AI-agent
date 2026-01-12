import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))      
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir == False:
            return f'\nError: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif os.path.isfile(target_dir) == False:
            return f'\nError: "{file_path}" does not exist or is not a regular file'
        elif ".py" not in file_path:
            return f'\nError: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        if args is not None:
            command.extend(args)

        process_success = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        subprocess_string = ""
        if process_success.returncode != 0:
            subprocess_string += (f'\nProcess exited with code {process_success.returncode }')
        elif process_success.stdout == "" and process_success.stderr == "":
            subprocess_string += "\nNo output produced"
        else:
            subprocess_string += f'\nSTDOUT: {process_success.stdout}\nSTDERR: {process_success.stderr}'
        
        return subprocess_string
    except Exception as e:
        return f'\nError: {e}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs only python files in the allowed directory, and outputs their results in a STDOUT STDERR format",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={

            "file_path": types.Schema(
                type=types.Type.STRING,
                description="A string representing the relative path of the file.",
                ),

            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional list that contains items that will be added on to the original command.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Individual flags that can be optionally passed via args, these are extended on the command string before it's ran."
                    )
                ),

            },
        required=["file_path"]
        ),
    )
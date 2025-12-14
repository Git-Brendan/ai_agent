import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file. Overwrites any existing contents.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_full = os.path.abspath(full_path)
        abs_working = os.path.abspath(working_directory) 
    
        # verify and make directories
        if not abs_full.startswith(abs_working):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory' 
        if not os.path.exists(abs_full):
            directory = os.path.dirname(abs_full)
            os.makedirs(directory, exist_ok=True)

        # write content to file
        with open(full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

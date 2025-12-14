import os
from functions.config import MAX_CHAR_LIMIT
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads contents of files in the specified directory up to 10,000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_full = os.path.abspath(full_path)
        abs_working = os.path.abspath(working_directory) 
    
        # verify directories
        if not abs_full.startswith(abs_working):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory' 
        if not os.path.isfile(abs_full):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # return string of content
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHAR_LIMIT + 1)
            if len(file_content_string) > MAX_CHAR_LIMIT:
                file_content_string = file_content_string[:MAX_CHAR_LIMIT]
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHAR_LIMIT} characters]'
        return file_content_string

    except Exception as e:
        return f"Error: {e}"




import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Spawn new processes, connect to their input/output/error pipes, and obtain their return codes. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []

    try:
        full_path = os.path.join(working_directory, file_path)
        abs_full = os.path.abspath(full_path)
        abs_working = os.path.abspath(working_directory)

        if not abs_full.startswith(abs_working):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_full):
            return f'Error: File "{file_path}" not found.'
        if not abs_full.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        command = ["python", file_path] + args
        completed_process = subprocess.run(
            command,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=working_directory,
        )

        # just return stdout + stderr, nothing else
        return completed_process.stdout + completed_process.stderr

    except Exception as e:
        return f"Error: executing python file: {e}"
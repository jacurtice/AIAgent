import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = abs_working_dir
    if file_path:
        target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            ['python3', target_file],
            capture_output=True,
            text=True
        )
    except Exception as e:
        return f"Error running Python file: {e}"
    
    output = f'STDOUT: {result.stdout}\n'
    output += f'STDERR: {result.stderr}\n'
    if result.returncode != 0:
        output += f" Process exited with code {result.returncode}\n"

    return output

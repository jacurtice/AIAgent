import os

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = abs_working_dir
    if file_path:
        target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000

    file_content_string = ""
    truncated = False
    if os.path.getsize(target_file) > MAX_CHARS:
        truncated = True
    
    print(f"Reading file: {target_file} (truncated={truncated})")
    try:
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except Exception as e:
        return f"Error reading file: {e}"
    
    if truncated:
        file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
    return file_content_string
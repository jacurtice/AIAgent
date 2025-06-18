import os

def get_files_info(working_directory, directory=None):
    if not directory:
        return f'Error: directory does not exist'
    
    path = os.path.join(working_directory, directory)
    print(f"Working directory: {working_directory}, Directory: {directory}, Path: {path}")

    if not os.path.exists(path):
        return f'Error: "{path}" does not exist'
    
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'
    
    absworking_directory = os.path.abspath(working_directory)
    absdirectory = os.path.abspath(path)
    print(f"Absolute working directory: {absworking_directory}, Absolute directory: {absdirectory}")

    if not absdirectory.startswith(absworking_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    files = os.listdir(path)
    if not files:
        return f'No files found in "{directory}"'
    
    try:
        files_info = []
        for file in files:
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                files_info.append(f"- {file}: file_size={size} bytes, is_dir=False")
            elif os.path.isdir(file_path):
                files_info.append(f"- {file}: file_size={size} bytes, is_dir=True")
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"
    
    

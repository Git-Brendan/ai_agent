import os

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        abs_full = os.path.abspath(full_path)
        abs_working = os.path.abspath(working_directory) 
    
        # verify directories
        if not abs_full.startswith(abs_working):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_full):
            return f'Error: "{directory}" is not a directory'

        # return strings of contents
        dir_contents = os.listdir(abs_full)
        contents_list = []
        for content in dir_contents:
            content_path = os.path.join(abs_full, content)
            cont_info = f'- {content}: file_size={os.path.getsize(content_path)} bytes, is_dir={os.path.isdir(content_path)}'
            contents_list.append(cont_info)
        return "\n".join(contents_list)

    except Exception as e:
        return f"Error: {e}"

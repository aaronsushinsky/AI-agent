import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))      
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir == False:
            return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

        elif os.path.isdir(target_dir) == False:
            return (f'Error: "{target_dir}" is not a directory')

        dir_record = []
        for name in os.listdir(target_dir):
            item_path = os.path.join(target_dir, name)
            dir_record.append(
            f"- {name}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
            )
        return "\n".join(dir_record)
    except Exception as e:
        return f'Error: {e}'
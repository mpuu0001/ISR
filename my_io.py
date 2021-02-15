import os
import shutil

def read(file_path: str) -> str:
    """Read a text file"""
    f = open(file_path, "r")
    content = f.read()
    f.close()
    return content


def write(file_path: str, content: str, model: str) -> None:
    """write into a text file"""
    f = open(file_path, model)
    f.write(content)
    f.close()


def make_directory(dir_path: str) -> None:
    """Make a new directory"""
    try:
        os.makedirs(dir_path)
    except OSError:
        pass
        os.chdir(dir_path)


def get_file_id(path: str) -> int:
    """Get file id"""
    lst = list(path.split('_'))
    lst = list(lst[1].split('.'))
    file_id = int(lst[0])
    return file_id


def remove_file(file_path: str) -> None:
    """Delete a file"""
    if os.path.exists(file_path):
        os.remove(file_path)


def remove_dir(dir_path: str) -> None:
    """Delete a directory"""
    shutil.rmtree(dir_path)
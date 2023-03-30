import shutil


def change_repository(path: str, new_path: str):
    try:
        shutil.copytree(path, new_path)
    except FileNotFoundError:
        pass

import json
from time import strftime, localtime
import os


def save_file(file: bytes, path: str, name: str):
    f = open(path + "/" + name, "wb")
    f.write(file)
    f.close()


def save_json(content, path: str, name: str):
    f = open(path + "/" + name, "w", encoding="utf-8")
    f.write(json.dumps(content, ensure_ascii=False))
    f.close()


def get_time() -> str:
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def delete_redundant_pictures(path: str, rate: int):
    files = sorted(os.listdir(path))
    name_length = len(files[0].split(".")[0])
    file_extension = files[0].split(".")[1]
    i = 0
    for file in files:
        if i % rate:
            os.remove(os.path.join(path, file))
        i += 1

    deleted_files = sorted(os.listdir(path))
    i = 0
    for file in deleted_files:
        os.rename(os.path.join(path, file), os.path.join(path, f"{i:0>{name_length}}.{file_extension}"))
        i += 1


def delete_frame(path: str, max_frame: int):
    files = sorted(os.listdir(path))
    if len(files) > max_frame:
        for file in files[max_frame:]:
            os.remove(os.path.join(path, file))
        return True
    return False

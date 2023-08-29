import json
from time import strftime, localtime


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

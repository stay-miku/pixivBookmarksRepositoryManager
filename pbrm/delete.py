import shutil
import error
import os


def delete(path: str):
    shutil.rmtree(path)


def delete_illust(pid: str, path: str):
    illusts = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    if pid not in illusts:
        raise error.IllustNotExists("pid " + pid + " is not existed")

    delete(path + "/" + pid)

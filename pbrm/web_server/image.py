from .. import config
import os
from bottle import static_file, abort
import re


def get_file(path, file_name):
    result = []
    for file in os.listdir(path):
        if re.match(f"^{re.escape(file_name)}\..*", file, re.IGNORECASE):
            result.append(file)

    return result


def get_image(pid, page):
    path = os.path.join(config.repository_path, pid)
    if os.path.exists(path):
        file = get_file(path, f"{pid}_p{page}")
        if len(file) > 0:
            return static_file(file[0], path)

    abort(404, "file not found")


def get_ugoira(pid):
    path = os.path.join(config.repository_path, pid)
    if os.path.exists(path):
        file = os.path.join(path, f"{pid}.gif")
        if os.path.exists(file):
            return static_file(f"{pid}.gif", path)

    abort(404, "file not found")

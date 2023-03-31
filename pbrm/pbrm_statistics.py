import os
import json


def statistics_unavailable(path: str):
    s = []
    with open(os.path.join(path, "bookmarks.json"), "r", encoding="utf-8") as f:
        bookmarks = json.loads(f.read())
    for i in bookmarks["illust"]:
        if i["userId"] == 0:
            with open(path + "/" + str(i["id"]) + "/meta.json", "r", encoding="utf-8") as f:
                if json.loads(f.read())["userId"] == 0:
                    s.append(i["id"])
    return s


def statistics_unavailableSaved(path: str):
    s = []
    with open(os.path.join(path, "bookmarks.json"), "r", encoding="utf-8") as f:
        bookmarks = json.loads(f.read())
    for i in bookmarks["illust"]:
        if i["userId"] == 0:
            with open(path + "/" + str(i["id"]) + "/meta.json", "r", encoding="utf-8") as f:
                if json.loads(f.read())["userId"] != 0:
                    s.append(i["id"])
    return s


def statistics_saved(path: str):
    illusts = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    return illusts


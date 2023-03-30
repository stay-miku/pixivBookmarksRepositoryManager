import json
import os


cookie: str

ugoira: str

ffmpeg: str

repository_path: str


def load(path: str):
    global cookie
    global ugoira
    global ffmpeg
    if not os.path.exists(path):
        config = {"cookie": None, "ugoira": "raw", "ffmpeg": None, "repositoryPath": None}
        f = open(path, "w", encoding="utf-8")
        f.write(json.dumps(config, ensure_ascii=False))
        f.close()
        cookie = None
        ugoira = "img"
        ffmpeg = None
    else:
        f = open(path, "r", encoding="utf-8")
        j = f.read()
        f.close()
        js = json.loads(j)
        cookie = js["cookie"]
        ugoira = js["ugoira"]
        ffmpeg = js["ffmpeg"]


def change_cookie(c: str, path):
    config = {"cookie": c, "ugoira": ugoira, "ffmpeg": ffmpeg, "repositoryPath": repository_path}
    with open(os.path.join(path, "config.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(config))


def change_ugoira(u: str, path):
    config = {"cookie": cookie, "ugoira": u, "ffmpeg": ffmpeg, "repositoryPath": repository_path}
    with open(os.path.join(path, "config.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(config))


def change_repository(p: str, path):
    config = {"cookie": cookie, "ugoira": ugoira, "ffmpeg": ffmpeg, "repositoryPath": p}
    with open(os.path.join(path, "config.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(config))

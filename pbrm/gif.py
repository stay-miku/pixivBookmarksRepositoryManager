import json
import subprocess
import os
from pbrm import error


def img_to_gif(match_path: str, save_path: str, frame_rate: float):
    result = subprocess.run("ffmpeg -framerate {} -i {} -vf"
                            " \"split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse\" {}"
                            .format(str(frame_rate), match_path, save_path)
                            , stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        raise error.CommandRunError("stdout: " + result.stdout.decode()
                                    + "\n--------------------------\nstderr: " + result.stderr.decode())


def gif_illust(path: str):
    try:
        with open(os.path.join(path, "ugoira.json"), "r", encoding="utf-8") as f:
            ugoira_meta = json.loads(f.read())
    except FileNotFoundError:
        return

    with open(os.path.join(path, "log.json"), "r", encoding="utf-8") as f:
        name = json.loads(f.read())["pid"]

    if os.path.exists(os.path.join(path, name + ".gif")):
        return

    frame_rate = 1000 / ugoira_meta["frames"][0]["delay"]
    file_name = ugoira_meta["frames"][0]["file"]
    extension = file_name.split(".")[1]
    length = len(file_name.split(".")[0])

    img_to_gif(path + "/images/%0{}d.{}".format(str(length), extension), os.path.join(path, name + ".gif"), frame_rate)


def auto_transform(path: str):
    illusts = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    for i in illusts:
        gif_illust(os.path.join(path, i))

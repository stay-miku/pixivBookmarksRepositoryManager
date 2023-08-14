import zipfile
from . import config
import os


def zip_out(path: str):
    with zipfile.ZipFile(path, "w") as f:
        i = 0
        all_illusts = [f for f in os.listdir(config.repository_path) if os.path.isdir(os.path.join(config.repository_path, f))]
        for illust in all_illusts:
            pic = [f for f in os.listdir(os.path.join(config.repository_path, illust)) if len(f.lower().split(".")) >= 2 and f.lower().split(".")[1] != "json"]
            for p in pic:
                print("{} : {}".format(i, os.path.join(config.repository_path, illust, p)))
                f.write(os.path.join(config.repository_path, illust, p))



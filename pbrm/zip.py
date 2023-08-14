import zipfile
from . import config
import os
import shutil


def zip_out(path: str):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as f:
        i = 1
        j = 1
        all_illusts = [f for f in os.listdir(config.repository_path) if os.path.isdir(os.path.join(config.repository_path, f))]
        for illust in all_illusts:
            pic = [f for f in os.listdir(os.path.join(config.repository_path, illust)) if len(f.lower().split(".")) >= 2 and f.lower().split(".")[1] != "json"]
            m = 1
            for p in pic:
                print("{}-{} {} : {}".format(j, m, i, os.path.join(config.repository_path, illust, p)))
                base_name = os.path.basename(os.path.join(config.repository_path, illust, p))
                f.write(os.path.join(config.repository_path, illust, p), base_name)
                i += 1
                m += 1
            j += 1



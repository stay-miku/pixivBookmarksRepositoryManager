import os
import zipfile
import subprocess

from pbrm import spider
from pbrm import utils
from pbrm import error


def save_log(log, path: str):
    utils.save_json(log, path, "log.json")


def save_meta(meta, path: str):
    utils.save_json(meta, path, "meta.json")


def save_img(meta, path: str, cookie: str):
    log = {"available": True, "updateTime": utils.get_time(), "illustType": 0, "pid": meta["id"]}
    save_log(log, path)
    pages = spider.get_pages(meta["id"], cookie)

    # 保存所有图片
    for page in pages:
        url = page["urls"]["original"]
        file = spider.image_download(url)
        file_name = url.split("/")[-1]
        utils.save_file(file, path, file_name)


def save_manga(meta, path: str, cookie: str):
    save_img(meta, path, cookie)


def save_ugoira(meta, path: str, cookie: str, save_gif: bool):
    log = {"available": True, "updateTime": utils.get_time(), "illustType": 2, "pid": meta["id"]}
    save_log(log, path)
    if not os.path.exists(path + "/images"):
        os.mkdir(path + "/images")
    ugoira_meta = spider.get_ugoira_meta(meta["id"], cookie)
    utils.save_json(ugoira_meta, path, "ugoira.json")
    ugoira = spider.ugoira_download(ugoira_meta["originalSrc"])
    utils.save_file(ugoira, path + "/images", "ugoira.zip")
    with zipfile.ZipFile(path + "/images/ugoira.zip", "r") as zip_file:  # 解压压缩包
        zip_file.extractall(path + "/images")
    os.remove(path + "/images/ugoira.zip")

    # 转gif
    if save_gif:
        frame_rate = 1000 / ugoira_meta["frames"][0]["delay"]
        file_name = ugoira_meta["frames"][0]["file"]
        extension = file_name.split(".")[1]
        length = len(file_name.split(".")[0])

        # ffmpeg合成gif
        result = subprocess.run("ffmpeg -framerate {} -i {}/%0{}d.{} -vf"
                                " \"split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse\" {}.gif"
                                .format(str(frame_rate), path + "/images", str(length),
                                        extension, path + "/" + meta["id"])
                                , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise error.CommandRunError("stdout: " + result.stdout.decode()
                                        + "\n--------------------------\nstderr: " + result.stderr.decode())


def save_illust(pid: str, path: str, cookie: str, save_gif: bool, skip_download: bool, skip_meta: bool):
    meta = spider.get_illust_meta(pid, cookie)
    if not skip_download:
        if meta["illustType"] == 0:
            save_img(meta, path, cookie)
        elif meta["illustType"] == 1:
            save_manga(meta, path, cookie)
        elif meta["illustType"] == 2:
            save_ugoira(meta, path, cookie, save_gif)
        else:
            raise error.UnSupportIllustType("UnSupport type: " + str(meta["illustType"]))
    if not skip_meta:
        save_meta(meta, path)


# 无效作品get_meta时会抛出错误,必须单独适配
def save_unavailable(meta, path):
    save_meta(meta, path)
    log = {"available": False, "updateTime": utils.get_time(), "illustType": None, "pid": meta["id"]}
    save_log(log, path)
    save_meta(meta, path)


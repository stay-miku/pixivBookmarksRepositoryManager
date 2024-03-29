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


def save_img(meta, path: str, cookie: str, saving_log=True, max_size=10000):
    log = {"available": True, "updateTime": utils.get_time(), "illustType": 0, "pid": meta["id"]}
    if saving_log:
        save_log(log, path)
    pages = spider.get_pages(meta["id"], cookie)

    # 保存所有图片
    i = 0
    for page in pages:
        url = page["urls"]["original"]
        file = spider.image_download(url)
        file_name = url.split("/")[-1]
        utils.save_file(file, path, file_name)
        i += 1
        if i >= max_size:
            break

    return False


def save_manga(meta, path: str, cookie: str, saving_log=True, max_size=10000):
    return save_img(meta, path, cookie, saving_log, max_size)


def save_ugoira(meta, path: str, cookie: str, save_gif: bool, saving_log=True, max_frame_rate=10000
                , max_frame_num=10000):
    log = {"available": True, "updateTime": utils.get_time(), "illustType": 2, "pid": meta["id"]}
    if saving_log:
        save_log(log, path)
    if not os.path.exists(path + "/images"):
        os.mkdir(path + "/images")
    ugoira_meta = spider.get_ugoira_meta(meta["id"], cookie)
    if saving_log:
        utils.save_json(ugoira_meta, path, "ugoira.json")
    ugoira = spider.ugoira_download(ugoira_meta["originalSrc"])
    utils.save_file(ugoira, path + "/images", "ugoira.zip")
    with zipfile.ZipFile(path + "/images/ugoira.zip", "r") as zip_file:  # 解压压缩包
        zip_file.extractall(path + "/images")
    os.remove(path + "/images/ugoira.zip")

    # 转gif
    if save_gif:
        frame_rate = 1000 / ugoira_meta["frames"][0]["delay"]
        rate = int(frame_rate / max_frame_rate + 0.5)   # 四舍五入当前帧率对最大帧率的比值
        if rate < 1:
            rate = 1
        frame_rate = frame_rate / rate
        if rate > 1:
            utils.delete_redundant_pictures(os.path.join(path, "images/"), rate)
        delete_frame = utils.delete_frame(os.path.join(path, "images/"), max_frame_num)
        file_name = ugoira_meta["frames"][0]["file"]
        extension = file_name.split(".")[1]
        length = len(file_name.split(".")[0])

        # ffmpeg合成gif
        result = subprocess.run("ffmpeg -framerate {} -i {}/%0{}d.{} -vf"
                                " \"split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse\" {}.gif"
                                .format(str(frame_rate), path + "/images", str(length),
                                        extension, path + "/" + meta["id"])
                                , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if result.returncode != 0:
            raise error.CommandRunError("stdout: " + result.stdout.decode()
                                        + "\n--------------------------\nstderr: " + result.stderr.decode())

        if rate > 1 or delete_frame:
            return True

    return False


def save_illust(pid: str, path: str, cookie: str, save_gif: bool, skip_download: bool, skip_meta: bool
                , saving_log=True, max_ugoira_frame_rate=10000, max_ugoira_frame_num=10000):
    meta = spider.get_illust_meta(pid, cookie)
    if not skip_meta:
        save_meta(meta, path)
    if not skip_download:
        if meta["illustType"] == 0:
            return save_img(meta, path, cookie, saving_log)
        elif meta["illustType"] == 1:
            return save_manga(meta, path, cookie, saving_log)
        elif meta["illustType"] == 2:
            return save_ugoira(meta, path, cookie, save_gif, saving_log, max_ugoira_frame_rate, max_ugoira_frame_num)
        else:
            raise error.UnSupportIllustType("UnSupport type: " + str(meta["illustType"]))



# 无效作品get_meta时会抛出错误,必须单独适配
def save_unavailable(meta, path):
    save_meta(meta, path)
    log = {"available": False, "updateTime": utils.get_time(), "illustType": None, "pid": meta["id"]}
    save_log(log, path)
    save_meta(meta, path)


import requests
import json
import pbrm


# 通用header
header = {
    "cookie": "",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
    "referer": "",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "accept-encoding": "gzip, deflate, br",
    "accept": "*/*"
}

referer = "https://www.pixiv.net/artworks/{}"


# 获取动图数据
def get_ugoira_meta(pid: str, cookie: str):
    h = header
    h["cookie"] = cookie
    h["referer"] = referer.format(pid)

    meta_data = requests.get("https://www.pixiv.net/ajax/illust/{}/ugoira_meta".format(pid), headers=h) \
        .content.decode("utf-8")
    json_data = json.loads(meta_data)
    if json_data["error"]:
        raise pbrm.GetUgoiraMetaError(pid, json_data["message"])     # 抛出error

    return json_data["body"]


# 获取作品数据
def get_illust_meta(pid: str, cookie: str):
    h = header
    h["cookie"] = cookie
    h["referer"] = referer.format(pid)

    meta_data = requests.get("https://www.pixiv.net/ajax/illust/" + pid, headers=h).content.decode("utf-8")
    json_data = json.loads(meta_data)
    if json_data["error"]:
        raise pbrm.GetIllustMetaError(pid, json_data["message"])

    return json_data["body"]


def get_pages(pid: str, cookie: str):
    h = header
    h["referer"] = referer.format(pid)
    h["cookie"] = cookie
    pages_data = requests.get("https://www.pixiv.net/ajax/illust/{}/pages".format(pid), headers=h).content\
        .decode("utf-8")
    pages_json = json.loads(pages_data)
    if pages_json["error"]:
        raise pbrm.GetPagesError(pid, pages_json["message"])

    return pages_json["body"]

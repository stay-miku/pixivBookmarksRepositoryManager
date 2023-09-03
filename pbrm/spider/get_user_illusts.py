import requests
import json


def get_user_illusts(pid: str, cookie: str):
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "referer": "https://www.pixiv.net/users/{}/artworks".format(pid),
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": cookie
    }

    url = "https://www.pixiv.net/ajax/user/{}/profile/all?lang=zh".format(pid)

    response = requests.get(url, headers=header)
    response_json = json.loads(response.content.decode("utf-8"))
    r = []
    # 当对应的类型没有作品时,其为list,否则为dict
    if isinstance(response_json["body"]["illusts"], dict):
        r += list(response_json["body"]["illusts"].keys())
    if isinstance(response_json["body"]["manga"], dict):
        r += list(response_json["body"]["manga"].keys())

    return r


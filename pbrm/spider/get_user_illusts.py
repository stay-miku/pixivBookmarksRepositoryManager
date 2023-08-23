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

    url = "https://www.pixiv.net/ajax/user/{}/profile/all?lang=zh&version=6ef70395cd96e1ec38515f935cf09d2b4c977caf".format(pid)

    response = requests.get(url, headers=header)

    return list(json.loads(response.content.decode("utf-8"))["body"]["illusts"].keys())


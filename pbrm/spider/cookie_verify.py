import requests
import json
import pbrm
from lxml import etree


# 验证cookie可用性,可用会返回一个包含账号id和账号名的字典,否则抛出CookieVerifyError
def cookie_verify_legacy(cookie: str):
    header = {
        "cookie": cookie,
        "referer": "https://www.pixiv.net/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 Safari/537.36",
        "sec-fetch-dest": "document",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        # "accept-encoding": "gzip, deflate, br",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7"
    }
    http = requests.get("https://www.pixiv.net/", headers=header).content.decode("utf-8")
    content = etree.HTML(http).xpath("//script[@id=\"__NEXT_DATA__\"]/text()")
    preload_state = json.loads(content[0])["props"]["pageProps"]["serverSerializedPreloadedState"]
    user_data = json.loads(preload_state)["userData"]["self"]
    if user_data is None:
        raise pbrm.CookieVerifyError("cookie无效,需要更换cookie")
    return {"userId": user_data["id"], "userName": user_data["pixivId"]}


def cookie_verify(cookie: str):
    header = {
        "cookie": cookie,
        "referer": "https://www.pixiv.net/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 Safari/537.36"
    }

    content = requests.get("https://www.pixiv.net/rpc/notify_count.php?op=count_unread", headers=header).content.decode("utf-8")
    if content == "":
        raise pbrm.CookieVerifyError("cookie无效,需要更换cookie")

    try:
        j = json.loads(content)
        i = j["popboard"]
    except Exception:
        raise pbrm.CookieVerifyError("cookie无效,需要更换cookie")

    return {"userId": "unavailable", "userName": "unavailable"}

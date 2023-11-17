import requests
import json
import pbrm


# 单页作品数量,可以决定获取收藏时连接次数(设太高谁知道会发生生么)
one_page_count = 48


# 获取收藏列表返回字典,会抛出GetBookmarksError
def get_bookmarks(cookie: str, user: str):
    header = {
        "cookie": cookie,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) C"
                      "hrome/111.0.0.0 Safari/537.36",
        "referer": "https://www.pixiv.net/users/" + user + "/bookmarks/artworks",
        "sec-fetch-dest": "empty",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        # "accept-encoding": "gzip, deflate, br",
        "accept": "application/json",
        "x-user-id": user
    }
    total = 0
    page = 1
    bookmarks = {"total": 0, "illust": []}

    # 分页循环获取所有收藏作品
    while 1:
        resp = requests.get("https://www.pixiv.net/ajax/user/{}/illusts/bookmarks?tag=&offset={}&limit={}&rest=show"
                            .format(user, str((page - 1) * one_page_count), str(one_page_count)), headers=header)\
                            .content.decode("utf-8")
        json_data = json.loads(resp)
        if json_data["error"]:
            raise pbrm.GetBookmarksError(json_data["message"])
        if total == 0:
            total = json_data["body"]["total"]
        bookmarks["illust"] += json_data["body"]["works"]
        if page * one_page_count >= total:
            break
        page += 1

    bookmarks["total"] = total
    return bookmarks

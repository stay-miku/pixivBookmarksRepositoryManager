import requests


header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) C"
                  "hrome/111.0.0.0 Safari/537.36",
    "referer": "https://www.pixiv.net/",
    "sec-fetch-dest": "image",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    # "accept-encoding": "gzip, deflate, br",
    "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
}


# 图片的bytes,需自行根据链接判断图片格式
def image_download(url: str) -> bytes:
    # 不管怎么样把看起来比较有用的都塞进去~
    h = header

    return requests.get(url, headers=h).content


# 按理返回的是一个压缩包,需要后续处理
def ugoira_download(url: str) -> bytes:

    h = header
    h["origin"] = "https://www.pixiv.net"
    h["sec-fetch-dest"] = "empty"
    h["accept"] = "*/*"

    return requests.get(url, headers=h).content

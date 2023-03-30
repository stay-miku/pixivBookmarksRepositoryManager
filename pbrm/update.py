import json

import spider
import save_illust
import utils
import os
import delete


def work_exists(pid: str, path: str):
    return os.path.exists(path + "/" + pid)


# 失效的作品的id和userId是整形而不是字符串
def update(cookie: str, path: str, skip_download: bool, skip_meta: bool, force_update: bool, force_update_illust: bool
           , force_update_meta: bool, auto_remove: bool, save_gif: bool):

    if not (os.path.exists(path) and os.path.isdir(path)):
        os.mkdir(path)

    # 合并force_update_illust和force_update_meta
    if force_update_meta is True and force_update_illust is True:
        force_update = True
    user = spider.cookie_verify(cookie)
    bookmarks = spider.get_bookmarks(cookie, user["userId"])
    log = {"updateTime": utils.get_time(), "total": bookmarks["total"], "updated": 0, "unavailable": 0}
    print("userId: {} userName: {} total: {}".format(user["userId"], user["userName"], bookmarks["total"]))

    i = 0
    all_illust = []
    for illust in bookmarks["illust"]:
        i = i + 1
        all_illust.append(str(illust["id"]))
        print("update: " + str(illust["id"]) + " process: {}/{}".format(str(i), bookmarks["total"]))
        if not force_update:
            if work_exists(str(illust["id"]), path):
                if force_update_meta != force_update_illust and illust["userId"] != 0:
                    # 将force当skip用
                    log["updated"] += 1
                    save_illust.save_illust(illust["id"], path + "/" + illust["id"], cookie, save_gif
                                            , not force_update_illust, not force_update_meta)
                continue

        if not work_exists(str(illust["id"]), path):
            os.mkdir(path + "/" + str(illust["id"]))

        if illust["userId"] == 0:
            log["unavailable"] += 1
            save_illust.save_unavailable(illust, path + "/" + str(illust["id"]))
            continue

        save_illust.save_illust(illust["id"], path + "/" + illust["id"], cookie, save_gif, skip_download, skip_meta)

    if auto_remove:
        illusts = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        for i in illusts:
            if i not in all_illust:
                delete.delete(os.path.join(path, i))

    with open(os.path.join(path, "log.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(log))

    with open(os.path.join(path, "bookmarks.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(bookmarks))


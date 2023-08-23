from typing import List
from .spider import get_user_illusts, get_illust_meta
from . import config
from . import save_illust


def get_meta_tag(meta) -> List["str"]:
    tags = []
    illust_tags = meta["tags"]["tags"]
    for t in illust_tags:
        tags.append(t["tag"])
        if "translation" in t:
            translation = t["translation"]
            for key in translation:
                tags.append(translation[key])

    return tags


def user_download(user_id: str, path: str, tags: List[str], strict: bool, skip_manga: bool, skip_ugoira: bool
                  , skip_image: bool, max_image: int):
    illusts = get_user_illusts(user_id, config.cookie)
    print("当前作者共有{}个作品".format(len(illusts)))
    print(
        "{} {} {} {} {} {}".format("使用tag限制, tag限制为{},".format(" ".join(tags)) if len(tags) != 0 else "不使用tag限制"
                                   , "使用严格模式," if strict else "不使用严格模式"
                                   , "跳过漫画类型作品," if skip_manga else ""
                                   , "跳过动图类型作品," if skip_ugoira else ""
                                   , "跳过插画类型作品," if skip_image else ""
                                   , "单个作品下载图片数量上限为{}".format("无上限" if max_image > 9999 else max_image)))
    downloaded = 0
    for illust in illusts:
        print("获取作品{}数据...".format(illust), end="", flush=True)
        while 1:
            try:
                meta = get_illust_meta(illust, config.cookie)
                break
            except Exception as e:
                print("Error: " + str(e) + "重试...", end="", flush=True)

        print("获取成功...", end="", flush=True)
        if skip_manga and meta["illustType"] == 1:
            print("作品为漫画类型,跳过")
            continue
        if skip_ugoira and meta["illustType"] == 2:
            print("作品为动图类型,跳过")
            continue
        if skip_image and meta["illustType"] == 0:
            print("作品为插画类型,跳过")
            continue

        illust_tags = get_meta_tag(meta)
        illust_tags = [i.strip().lower() for i in illust_tags]
        tags = [i.strip().lower() for i in tags]

        if strict:
            tags_set = set(tags)
            illusts_tags_set = set(illust_tags)
            if not tags_set.issubset(illusts_tags_set):
                print("未符合tag要求(严格模式),跳过")
                continue

        else:
            contain = False
            for i in tags:
                if i in illust_tags:
                    contain = True
                    break
            if not contain:
                print("未符合tag要求,跳过")
                continue

        print("开始下载...", end="", flush=True)
        support = True
        while 1:
            try:
                if meta["illustType"] == 0:
                    save_illust.save_img(meta, path, config.cookie, False, max_image)
                elif meta["illustType"] == 1:
                    save_illust.save_manga(meta, path, config.cookie, False, max_image)
                elif meta["illustType"] == 2:
                    save_illust.save_ugoira(meta, path, config.cookie, config.ugoira == "gif", False)
                else:
                    support = False
                break
            except Exception as e:
                print("Error: " + str(e) + "重试...", end="", flush=True)

        if not support:
            print("不支持的作品类型: {}, 跳过".format(meta["illustType"]))
            continue
        downloaded += 1
        print("保存完毕")
    print("共保存了{}个作品".format(downloaded))

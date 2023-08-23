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
    for illust in illusts:
        print("获取作品{}数据...".format(illust), end="")
        meta = get_illust_meta(illust, config.cookie)
        print("获取成功...", end="")
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

        if strict:
            tags_set = set(tags)
            illusts_tags_set = set(illust_tags)
            if not tags_set.issubset(illusts_tags_set):
                print("未符合tag要求(严格模式),跳过")
                continue

        else:
            contain = False
            for i in tags:
                for j in illusts:
                    if i == j:
                        contain = True
                        break
                if contain:
                    break
            if not contain:
                print("未符合tag要求,跳过")
                continue

        print("开始下载...", end="")
        if meta["illustType"] == 0:
            save_illust.save_img(meta, path, config.cookie, False, max_image)
        elif meta["illustType"] == 1:
            save_illust.save_manga(meta, path, config.cookie, False, max_image)
        elif meta["illustType"] == 2:
            save_illust.save_ugoira(meta, path, config.cookie, config.ugoira == "gif", False)
        else:
            print("不支持的作品类型: {}, 跳过".format(meta["illustType"]))
            continue

        print("保存完毕")



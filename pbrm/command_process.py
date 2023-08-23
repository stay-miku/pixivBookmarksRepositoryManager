from typing import Dict
from pbrm import update
from pbrm import config
from pbrm import delete
from pbrm import change_repository
from pbrm import pbrm_statistics
from pbrm import gif
from . import zip
import os
from .save_illust import save_illust
from .user_download import user_download
from . import error
from . import spider


def cookie_verify(cookie="") -> bool:
    try:
        user = spider.cookie_verify(config.cookie if cookie == "" else cookie)
        print("cookie有效, userId: {}, userName: {}".format(user["userId"], user["userName"]))
        return True
    except error.CookieVerifyError:
        print("cookie无效,请使用pbrm config cookie <CONTENT>命令重新设置")
        return False


def command_process(args: Dict, script_path: str, work_path: str):
    if args["update"]:
        if not cookie_verify():
            return
        update.update(config.cookie, config.repository_path, args["--skip-download"], args["--skip-meta"]
                      , args["--force-update"], args["--force-update-illust"], args["--force-update-meta"]
                      , args["--auto-remove"], config.ugoira == "gif")

    elif args["delete"]:
        delete.delete_illust(args["<PID>"], config.repository_path)
        print("deleted")

    elif args["config"]:
        if args["<CONFIG>"] == "cookie":
            if args["<CONTENT>"] is None:
                print(config.cookie)
            else:
                config.change_cookie(args["<CONTENT>"], script_path)
                print("changed")
        elif args["<CONFIG>"] == "ugoira":
            if args["<CONTENT>"] is None:
                print(config.ugoira)
            elif args["<CONTENT>"] == "raw" or args["<CONTENT>"] == "gif":
                if args["<CONTENT>"] == "gif":
                    gif.auto_transform(config.repository_path)
                config.change_ugoira(args["<CONTENT>"], script_path)
                print("changed")
            else:
                print("unknown config content")
        else:
            print("unknown config")

    elif args["set"]:
        if args["<PATH>"] is None:
            print(config.repository_path)
        elif args["<PATH>"] == "this":
            change_repository.change_repository(config.repository_path, work_path)
            config.change_repository(work_path, script_path)
        else:
            change_repository.change_repository(config.repository_path, args["<PATH>"])
            config.change_repository(args["<PATH>"], script_path)

    elif args["show"]:
        if args["unavailable"]:
            if args["--only-number"]:
                print(len(pbrm_statistics.statistics_unavailable(config.repository_path)))
            else:
                for i in pbrm_statistics.statistics_unavailable(config.repository_path):
                    print(i)
        elif args["unavailableSaved"]:
            if args["--only-number"]:
                print(len(pbrm_statistics.statistics_unavailableSaved(config.repository_path)))
            else:
                for i in pbrm_statistics.statistics_unavailableSaved(config.repository_path):
                    print(i)
        elif args["saved"]:
            if args["--only-number"]:
                print(len(pbrm_statistics.statistics_saved(config.repository_path)))
            else:
                for i in pbrm_statistics.statistics_saved(config.repository_path):
                    print(i)

    elif args["zip"]:
        output_path = args["<OUT_PATH>"]
        if output_path.startswith("/"):
            pass
        else:
            output_path = os.path.join(work_path, output_path)

        zip.zip_out(output_path)

    elif args["download"]:
        if not cookie_verify():
            return
        if args["--illust"]:
            save_illust(args["<USER_ID>"], work_path, config.cookie, config.ugoira == "gif", False, True, False)
            print("completed")

        else:
            if args["--tags"]:
                tags = args["<TAG>"]
            else:
                tags = []

            user_download(args["<USER_ID>"], work_path, tags, args["--strict"], args["--no-manga"]
                          , args["--no-ugoira"], args["--no-image"]
                          , int(args["<MAX_SIZE>"]) if args["--max"] else 10000)

    elif args["cookie"]:
        try:
            user = spider.cookie_verify(config.cookie if args["<COOKIE>"] is None else args["<COOKIE>"])
            print("cookie有效, userId: {}, userName: {}".format(user["userId"], user["userName"]))
        except error.CookieVerifyError:
            print("cookie无效")

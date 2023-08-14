from typing import Dict
from pbrm import update
from pbrm import config
from pbrm import delete
from pbrm import change_repository
from pbrm import pbrm_statistics
from pbrm import gif
from . import zip
import os


def command_process(args: Dict, script_path: str, work_path: str):
    if args["update"]:
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
        if output_path.startwith("/"):
            pass
        else:
            output_path = os.path.join(work_path, output_path)

        zip.zip_out(output_path)

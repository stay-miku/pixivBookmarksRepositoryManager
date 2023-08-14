import docopt
from pbrm import command_process
from pbrm import config
import os

doc = """Pixiv Bookmarks Repository Manager

Usage:
    pbrm update [-dmafin]
    pbrm delete <PID>
    pbrm config <CONFIG> [<CONTENT>]
    pbrm set [<PATH>]
    pbrm show (unavailable | unavailableSaved | saved) [-o]
    pbrm zip <OUT_PATH>

Options:
    -d, --skip-download             跳过下载作品(仍会下载meta)
    -m, --skip-meta                 跳过下载meta数据
    -a, --auto-remove               更新同时删除已取消收藏的作品
    -f, --force-update              强制更新所有收藏(已保存的收藏将会重新下载，会跳过已失效的收藏)
    -i, --force-update-illust       强制更新作品本体
    -n, --force-update-meta         强制更新所有meta数据
    -o, --only-number               只显示作品数量而不是显示作品id
    
    <PID>                           作品id
    <CONFIG>                        配置项,可配置项为cookie,ugoira(动图保存方式,对应CONTENT有raw和gif,分别是多张图片保存和需要ffmpeg的gif保存)
    <CONTENT>                       配置项对应内容,为空时是查看配置
    <PATH>                          仓库位置路径,为空时为显示仓库路径,为this是使用当前路径,其余为指定路径
    <OUT_PATH>                      输出的zip文件路径和名称,如./output.zip
    
    update                          更新收藏
    delete                          删除指定收藏(仅支持pid指定)
    config                          查看或修改配置
    set                             设置仓库路径
    show                            显示统计信息
    unavailable                     失效且未保存的作品
    unavailableSaved                失效但已保存的作品
    saved                           已保存的作品
    zip                             将备份的作品打包到zip文件中

"""


def main():
    args = docopt.docopt(doc, version="Pixiv Bookmarks Repository Manager 0.0.1")
    work_path = os.getcwd().replace("\\", "/")
    script_path = os.path.dirname(__file__).replace("\\", "/")
    config.load(script_path + "/config.json")
    command_process.command_process(args, script_path, work_path)


if __name__ == "__main__":
    main()

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
    pbrm download <USER_ID> [-t <TAG>... [-s]] [-l] [--no-manga] [--no-ugoira] [--no-image] [--max <MAX_SIZE>]
    pbrm cookie [<COOKIE>]

Options:
    -d, --skip-download             跳过下载作品(仍会下载meta)
    -m, --skip-meta                 跳过下载meta数据
    -a, --auto-remove               更新同时删除已取消收藏的作品
    -f, --force-update              强制更新所有收藏(已保存的收藏将会重新下载，会跳过已失效的收藏)
    -i, --force-update-illust       强制更新作品本体
    -n, --force-update-meta         强制更新所有meta数据
    -o, --only-number               只显示作品数量而不是显示作品id
    -t, --tags                      按tag下载作品
    -l, --illust                    使用此参数后USER_ID会被作为作品pid下载对应作品
    -s, --strict                    匹配tag为严格模式,只有作品包含所有给出的tag才会下载,不使用此选项则只要作品包含给出的任一tag都会下载
    --no-manga                      下载作品时会跳过漫画类型,tip:目前download操作不会下载漫画类型(除非--illust),此参数目前无效
    --no-ugoira                     下载作品时会跳过动图类型
    --no-image                      下载作品时会跳过插画类型
    --max                           下载有多张图片的插画或漫画时,下载图片数量的上限
    
    <PID>                           作品id
    <CONFIG>                        配置项,可配置项为cookie,ugoira(动图保存方式,对应CONTENT有raw和gif,分别是多张图片保存和需要ffmpeg的gif保存)
    <CONTENT>                       配置项对应内容,为空时是查看配置
    <PATH>                          仓库位置路径,为空时为显示仓库路径,为this是使用当前路径,其余为指定路径
    <OUT_PATH>                      输出的zip文件路径和名称,如./output.zip
    <USER_ID>                       作者的user id
    <TAG>                           单个tag,建议使用相应作者作品下显示的tag,否则可能无法匹配
    <COOKIE>                        可选项,若不填则检测当前所配置的cookie,填了就检测参数所提供的cookie
    
    update                          更新收藏
    delete                          删除指定收藏(仅支持pid指定)
    config                          查看或修改配置
    set                             设置仓库路径
    show                            显示统计信息
    unavailable                     失效且未保存的作品
    unavailableSaved                失效但已保存的作品
    saved                           已保存的作品
    zip                             将备份的作品打包到zip文件中
    download                        下载某个作者的作品,保存到当前文件夹(也需要配置cookie)
    cookie                          测试当前cookie可用性

"""


def main():
    args = docopt.docopt(doc, version="Pixiv Bookmarks Repository Manager 0.0.12")
    work_path = os.getcwd().replace("\\", "/")
    script_path = os.path.dirname(__file__).replace("\\", "/")
    config.load(script_path + "/config.json")
    command_process.command_process(args, script_path, work_path)


if __name__ == "__main__":
    main()

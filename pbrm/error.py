# 获取元数据错误


class PixivGetError(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return "Error Message: " + self.message


class GetMetaError(PixivGetError):
    pid: str  # 作品id

    def __init__(self, pid: str, message: str):
        self.pid = pid
        self.message = message

    def __str__(self):
        return "illustId: " + self.pid + " message: " + self.message


class GetIllustMetaError(GetMetaError):
    pass


class GetUgoiraMetaError(GetMetaError):
    pass


class GetPagesError(GetMetaError):
    pass


class GetBookmarksError(PixivGetError):
    pass


class CookieVerifyError(PixivGetError):
    pass


class UnSupportIllustType(PixivGetError):
    pass


class CommandRunError(PixivGetError):
    pass


class IllustNotExists(PixivGetError):
    pass

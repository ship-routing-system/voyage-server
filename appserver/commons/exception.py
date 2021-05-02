class BaseError(Exception):
    status_code = 500
    msg = ""

    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class RequestError(BaseError):
    """ 클라이언트 서버에서 잘못된 호출 형식으로 올렸을 경우
    """

    status_code = 400


class ServerError(BaseError):
    """ 서버 내 이슈로 결과를 올바르게 처리하지 못한 경우
    """
    status_code = 500

class FTSException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload


class BadRequest(FTSException):
    def __init__(self, message):
        super().__init__(message, 400)

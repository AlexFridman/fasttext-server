class ApiException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload


class BadRequest(ApiException):
    def __init__(self, message):
        super().__init__(message, 400)

class LangIsNotSupported(ApiException):
    def __init__(self):
        super().__init__('Language is not supported', 404)

class IntentClassificationError(ApiException):
    def __init__(self):
        super().__init__('Classification error', 500)

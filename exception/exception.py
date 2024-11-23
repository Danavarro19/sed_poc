class AuthenticationException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)

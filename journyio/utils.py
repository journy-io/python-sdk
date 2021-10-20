from collections import defaultdict
from enum import Enum


class APIError(Enum):
    ServerError = 1, "ServerError"
    UnauthorizedError = 2, "UnauthorizedError"
    BadArgumentsError = 3, "BadArgumentsError"
    TooManyRequests = 4, "TooManyRequests"
    NotFoundError = 5, "NotFoundError"
    UnknownError = 6, "UnknownError"
    ForbiddenError = 7, "ForbiddenError"
    UnprocessableError = 8, "Unprocessable"


class JournyException(Exception):
    def __init__(self, msg: str):
        assert isinstance(msg, str)
        super().__init__(msg)

        self.msg = msg

    def __str__(self):
        return f"JournyException({self.msg})"


status_code_to_api_error_mapping = defaultdict(lambda: APIError.UnknownError)
status_code_to_api_error_mapping.update(
    {
        400: APIError.BadArgumentsError,
        401: APIError.UnauthorizedError,
        403: APIError.ForbiddenError,
        404: APIError.NotFoundError,
        422: APIError.UnprocessableError,
        429: APIError.TooManyRequests,
        500: APIError.ServerError,
    }
)


def status_code_to_api_error(status_code: int):
    assert_journy(isinstance(status_code, int), "The status_code is not an int.")
    return status_code_to_api_error_mapping[status_code]


def assert_journy(value, message):
    if not value:
        raise JournyException(message)

from .results import APIError
from collections import defaultdict


class JournyException(Exception):

    def __init__(self, msg: str):
        assert (isinstance(msg, str))

        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return f"JournyException({self.msg})"


status_code_to_api_error_mapping = defaultdict(lambda _: APIError.UnknownError)
status_code_to_api_error_mapping.update({401: APIError.UnauthorizedError,
                                         400: APIError.BadArgumentsError,
                                         429: APIError.TooManyRequests,
                                         404: APIError.NotFoundError,
                                         500: APIError.ServerError})


def status_code_to_api_error(status_code: int):
    assert (isinstance(status_code, int))

    return status_code_to_api_error_mapping.get(status_code)

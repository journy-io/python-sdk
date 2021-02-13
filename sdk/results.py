from enum import Enum
from typing import TypeVar, Generic

T = TypeVar('T')


class Success(Generic[T]):
    """
    Success object, returned by the client if the call to the API succeeded.
    The data optionally contains a
    """

    def __init__(self, request_id: str, calls_remaining: int, data: T):
        assert (isinstance(request_id, str))
        assert (isinstance(calls_remaining, int))

        self.request_id = request_id
        self.calls_remaining = calls_remaining
        self.data = data

    def __str__(self):
        return f"Success({self.request_id}, {self.calls_remaining}, {self.data})"

    def __repr__(self):
        return self.__str__()


class APIError(Enum):
    ServerError = "ServerError"
    UnauthorizedError = "UnauthorizedError"
    BadArgumentsError = "BadArgumentsError"
    TooManyRequests = "TooManyRequests"
    NotFoundError = "NotFoundError"
    UnknownError = "UnknownError"


class Failure(object):
    """
    Failure object, returned by the client if the call to the API did not succeed.
    """

    def __init__(self, request_id: str or None, calls_remaining: int or None, error: APIError):
        if request_id:
            assert (isinstance(request_id, str))
        if calls_remaining:
            assert (isinstance(calls_remaining, int))
        assert (isinstance(error, APIError))

        self.request_id = request_id
        self.calls_remaining = calls_remaining
        self.error = error

    def __str__(self):
        return f"Error({self.request_id}, {self.calls_remaining}, {self.error})"

    def __repr__(self):
        return self.__str__()


class TrackingSnippetResponse(object):

    def __init__(self, domain: str, snippet: str):
        assert (isinstance(domain, str))
        assert (isinstance(snippet, str))
        self.domain = domain
        self.snippet = snippet


class ApiKeyDetails(object):

    def __init__(self, permissions: list):
        assert (isinstance(permissions, list))
        for permission in permissions:
            assert (isinstance(permission, str))
        self.permissions = permissions

from enum import Enum
from typing import TypeVar, Generic

from sdk.utils import assert_journy

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
    ServerError = 1, "ServerError"
    UnauthorizedError = 2, "UnauthorizedError"
    BadArgumentsError = 3, "BadArgumentsError"
    TooManyRequests = 4, "TooManyRequests"
    NotFoundError = 5, "NotFoundError"
    UnknownError = 6, "UnknownError"


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
        assert_journy(isinstance(domain, str), "The domain is not a string.")
        assert_journy(isinstance(snippet, str), "The request is not a string.")
        self.domain = domain
        self.snippet = snippet

    def __str__(self):
        return f"TrackingSnippetResponse({self.domain}, {self.snippet})"

    def __repr__(self):
        return self.__str__()


class LinkResponse(object):
    def __init__(self, message: str):
        assert_journy(isinstance(message, str), "The message is not a string.")
        self.message = message

    def __str__(self):
        return f"LinkResponse({self.message})"

    def __repr__(self):
        return self.__str__()


class ApiKeyDetails(object):

    def __init__(self, permissions: list):
        assert_journy(isinstance(permissions, list), "Permissions is not a list.")
        for permission in permissions:
            assert (isinstance(permission, str))
        self.permissions = permissions

    def __str__(self):
        return f"ApiKeyDetails({self.permissions})"

    def __repr__(self):
        return self.__str__()

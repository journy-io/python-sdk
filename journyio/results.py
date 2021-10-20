from typing import TypeVar, Generic

from journyio.utils import assert_journy, APIError

T = TypeVar("T")


class Success(Generic[T]):
    """
    Success object, returned by the client if the call to the API succeeded.
    The data optionally contains a
    """

    def __init__(self, request_id: str, calls_remaining: int, data: T):
        assert_journy(isinstance(request_id, str), "request_id is not a string.")
        assert_journy(isinstance(calls_remaining, int), "calls_remaining is not an int")

        self.request_id = request_id
        self.calls_remaining = calls_remaining
        self.data = data

    def __str__(self):
        return f"Success({self.request_id}, {self.calls_remaining}, {self.data})"

    def __repr__(self):
        return self.__str__()


class Failure(object):
    """
    Failure object, returned by the client if the call to the API did not succeed.
    """

    def __init__(
        self, request_id: str or None, calls_remaining: int or None, error: APIError
    ):
        if request_id:
            assert_journy(isinstance(request_id, str), "request_id is not a string.")
        if calls_remaining:
            assert_journy(
                isinstance(calls_remaining, int), "calls_remaining is not an int."
            )
        assert_journy(isinstance(error, APIError), "error is no APIError object.")

        self.request_id = request_id
        self.calls_remaining = calls_remaining
        self.error = error

    def __str__(self):
        return f"Failure({self.request_id}, {self.calls_remaining}, {self.error})"

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


class ApiKeyDetails(object):
    def __init__(self, permissions: list):
        assert_journy(isinstance(permissions, list), "Permissions is not a list.")
        for permission in permissions:
            assert_journy(
                isinstance(permission, str), "Permissions is not a list of strings."
            )
        self.permissions = permissions

    def __str__(self):
        return f"ApiKeyDetails({self.permissions})"

    def __repr__(self):
        return self.__str__()

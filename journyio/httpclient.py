import json
from collections import defaultdict
from enum import Enum

import requests

from .utils import JournyException, assert_journy


class Method(Enum):
    GET = 1
    POST = 2
    DELETE = 3
    PUT = 4
    HEAD = 5
    PATCH = 6


class HttpHeaders(dict):
    def __init__(self):
        super().__init__()
        self.headers = defaultdict(lambda _: None)

    def __getitem__(self, key: str):
        assert_journy(isinstance(key, str), "The key is not a string.")

        return self.headers.get(key.lower().strip())

    def __setitem__(self, key: str, value: str or list):
        assert_journy(isinstance(key, str), "The key is not a string.")
        assert_journy(
            isinstance(value, str)
            or (isinstance(value, list) and all(isinstance(val, str) for val in value)),
            "Value is not a string or a list of strings.",
        )
        self.headers.__setitem__(key.lower().strip(), value)

    def union(self, other):
        self.headers.update(other.headers)
        return self

    def __str__(self):
        return json.dumps(self.headers)

    def __repr__(self):
        return self.__str__()


class HttpRequest(object):
    def __init__(
        self,
        url: str,
        method: Method = Method.GET,
        headers: HttpHeaders or None = None,
        body=None,
    ):
        if headers is None:
            headers = HttpHeaders()

        assert_journy(isinstance(url, str), "The url is not a string.")
        assert_journy(isinstance(method, Method), "The method is not a Method object.")
        assert_journy(
            isinstance(headers, HttpHeaders), "The headers is not a HttpHeaders object."
        )

        self.url = url
        self.method = method
        self.headers = headers
        self.body = body

    def __str__(self):
        return f"HttpRequest({self.url}, {self.method}, {self.headers}, {self.body})"

    def __repr__(self):
        return self.__str__()


class HttpResponse(object):
    def __init__(
        self, status_code: int = 200, headers: HttpHeaders or None = None, body=None
    ):
        if headers is None:
            headers = HttpHeaders()

        assert_journy(isinstance(status_code, int), "The status_code is not an int.")
        assert_journy(
            isinstance(headers, HttpHeaders),
            "The headers parameter is not a HttpHeaders object.",
        )

        if not (100 <= status_code <= 599):
            raise JournyException("Status code is invalid.")

        self.status_code = status_code
        self.headers = headers
        self.body = body

    def __str__(self):
        return f"HttpResponse({self.status_code}, {self.headers}, {self.body})"

    def __repr__(self):
        return self.__str__()


class HttpClient:
    """
    Interface for a HttpClient
    """

    def send(self, request: HttpRequest):
        pass


class HttpClientRequests(HttpClient):
    def __init__(self):
        self.methods = {
            Method.GET: requests.get,
            Method.POST: requests.post,
            Method.PUT: requests.put,
            Method.DELETE: requests.delete,
            Method.HEAD: requests.head,
            Method.PATCH: requests.patch,
        }

    def send(self, request: HttpRequest):
        assert_journy(
            isinstance(request, HttpRequest),
            "The request is not an HttpRequest object.",
        )

        method = self.methods[request.method]
        if not method:
            raise JournyException("No correct method was given.")
        try:
            response = method(
                request.url, headers=request.headers.headers, data=request.body
            )
            headers = HttpHeaders()
            for header in response.headers:
                headers[header] = response.headers[header]
            return HttpResponse(
                response.status_code, headers, json.loads(response.text)
            )
        except:
            raise JournyException(
                "An unknown error has occurred while performing the API request."
            )

    def __str__(self):
        return f"HttpClient()"

    def __repr__(self):
        return self.__str__()


class HttpClientTesting(HttpClient):
    def __init__(self, dummy_response: HttpResponse):
        self.dummy_response = dummy_response
        self.received_request = None

    def send(self, request: HttpRequest):
        assert_journy(
            isinstance(request, HttpRequest),
            "The request is not an HttpRequest object.",
        )
        assert_journy(
            isinstance(request.method, Method), "The method is not an Method object."
        )
        assert_journy(isinstance(request.url, str), "The url is not a string.")
        assert_journy(
            isinstance(request.headers, HttpHeaders),
            "The headers is not an HttpHeaders object.",
        )

        self.received_request = request
        return self.dummy_response

    def __str__(self):
        return f"HttpClientTesting({self.dummy_response}, {self.received_request})"

    def __repr__(self):
        return self.__str__()

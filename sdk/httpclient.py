import requests
from enum import Enum
from collections import defaultdict

from .utils import JournyException


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
        if not isinstance(key, str):
            raise JournyException("The key is not a string.")
        return self.headers.get(key.lower().strip())

    def __setitem__(self, key: str, value: str or list):
        if not isinstance(key, str):
            raise JournyException("The key is not a string.")
        if isinstance(value, str) or (isinstance(value, list) and all(isinstance(val, str) for val in value)):
            self.headers.__setitem__(key.lower().strip(), value)  # TODO: thoroughly test this!
        else:
            raise JournyException("Value is not a string or a list of strings.")

    def union(self, other):
        self.headers.update(other.headers)
        return self


class HttpRequest(object):

    def __init__(self, url: str, method: Method = Method.GET, headers: HttpHeaders or None = None, body=None):
        if headers is None:
            headers = HttpHeaders()

        assert (isinstance(url, str))
        assert (isinstance(method, Method))
        assert (isinstance(headers, HttpHeaders))

        self.url = url
        self.method = method
        self.headers = headers
        self.body = body

    def __str__(self):
        return f"HttpRequest({self.url}, {self.method}, {self.headers}, {self.body})"

    def __repr__(self):
        return self.__str__()


class HttpResponse(object):

    def __init__(self, status_code: int = 200, headers: HttpHeaders or None = None, body=None):
        if headers is None:
            headers = HttpHeaders()

        assert (isinstance(status_code, int))
        assert (isinstance(headers, HttpHeaders))

        if not (100 <= status_code <= 599):
            raise JournyException("Status code is invalid.")

        self.status_code = status_code
        self.headers = headers
        self.body = body

    def __str__(self):
        return f"HttpResponse({self.status_code}, {self.headers}, {self.body})"

    def __repr__(self):
        return self.__str__()


class HttpClient(object):

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
        assert (isinstance(request, HttpRequest))

        method = self.methods[request.method]
        if not method:
            raise JournyException("No correct method was given.")
        try:
            response = method(request.url, headers=request.headers, data=request.body)
            return HttpResponse(response.status_code, response.headers, response.text)
        except:
            raise JournyException("An unknown error has occurred while performing the API request.")

    def __str__(self):
        return f"HttpClient()"

    def __repr__(self):
        return self.__str__()


class HttpClientTesting(object):

    def __init__(self, dummy_response: HttpResponse):
        self.dummy_response = dummy_response
        self.received_request = None

    def send(self, request: HttpRequest):
        assert (isinstance(request, HttpRequest))
        assert (isinstance(request.method, Method))
        assert (isinstance(request.url, str))
        assert (isinstance(request.headers, HttpHeaders))

        self.received_request = request
        return self.dummy_response

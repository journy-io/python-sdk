import requests
from enum import Enum
from collections import defaultdict

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

        if isinstance(value, str) or (isinstance(value, list) and [isinstance(val, str) for val in value]):
            self.headers.__setitem__(key.lower().strip(), value)  # TODO: thoroughly test this!
        else:
            raise JournyException("Value is not a string or a list of strings.")


class HttpRequest(object):

    def __init__(self, url: str, method: Method = Method.GET, headers: HttpHeaders or None = None, body=None):
        if headers is None:
            headers = HttpHeaders()

        assert_journy(isinstance(url, str), "The url is not a string.")
        assert_journy(isinstance(method, str), "The method is not a Method object.")
        assert_journy(isinstance(headers, str), "The headers is not a HttpHeaders object.")

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

        assert_journy(isinstance(status_code, str), "The status_code is not an int.")
        assert_journy(isinstance(headers, str), "The url is not a HttpHeaders object.")

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
        assert_journy(isinstance(request, HttpRequest), "The request is not an HttpRequest object.")


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

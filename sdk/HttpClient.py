import requests
from enum import Enum


class Method(Enum):
    GET = 1
    POST = 2
    DELETE = 3
    PUT = 4
    HEAD = 5
    PATCH = 6


class HttpRequest(object):

    def __init__(self, url, method=Method.GET, headers=None, body=None):
        if headers is None:
            headers = {}
        assert (isinstance(url, str))
        assert (isinstance(method, Method))
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body

    def __str__(self):
        return f"HttpRequest({self.url}, {self.method}, {self.headers}, {self.body})"

    def __repr__(self):
        return self.__str__()


class HttpResponse(object):

    def __init__(self, status_code=200, headers=None, body=""):
        assert (isinstance(status_code, int))
        assert (isinstance(body, str))
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

    def send(self, request):
        assert (isinstance(request, HttpRequest))
        method = self.methods[request.method]
        if not method:
            raise Exception("No correct method given.")
        response = method(request.url, headers=request.headers, data=request.body)
        return HttpResponse(response.status_code, response.headers, response.text)

    def __str__(self):
        return f"HttpClient()"

    def __repr__(self):
        return self.__str__()

# TODO: Add more validation

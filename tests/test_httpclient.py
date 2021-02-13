import pytest

from sdk.httpclient import HttpHeaders, HttpRequest, HttpResponse, HttpClient, Method
from sdk.utils import JournyException


def test_http_headers():
    pass


def test_http_request():
    request = HttpRequest("https://journy.io", Method.GET, None, None)

    assert (request.url == "https://journy.io")
    assert (request.method is Method.GET)
    assert (request.headers == HttpHeaders())

    assert (request.__str__() == "HttpRequest(https://journy.io, Method.GET, {}, None)")

    with pytest.raises(AssertionError):
        HttpRequest(123, Method.GET, HttpHeaders(), None)
    with pytest.raises(AssertionError):
        HttpRequest("https://journy.io", 123, HttpHeaders(), None)
    with pytest.raises(AssertionError):
        HttpRequest("https://journy.io", Method.GET, 123, None)


def test_http_response():
    response = HttpResponse(200, HttpHeaders(), None)

    assert (response.status_code is 200)
    assert (response.headers == HttpHeaders())

    assert (response.__str__() == "HttpResponse(200, {}, None)")

    with pytest.raises(AssertionError):
        HttpResponse("200", HttpHeaders(), None)
    with pytest.raises(AssertionError):
        HttpResponse(200, 213, None)
    with pytest.raises(JournyException):
        HttpResponse(1000, HttpHeaders(), None)


def test_http_client():
    client = HttpClient()

    with pytest.raises(AssertionError):
        client.send(123)

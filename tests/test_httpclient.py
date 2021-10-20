import pytest

from journyio.httpclient import (
    HttpHeaders,
    HttpRequest,
    HttpResponse,
    HttpClientRequests,
    Method,
    HttpClientTesting,
)
from journyio.utils import JournyException


def test_http_headers():
    headers = HttpHeaders()
    assert headers["doesnotexist"] is None
    headers["doesexist"] = "hallo"
    assert headers["doesexist"] == "hallo"
    headers["thistoo"] = ["a", "b"]
    assert headers["thistoo"]
    with pytest.raises(JournyException):
        headers[2] = "hallo"
    with pytest.raises(JournyException):
        headers["doesexist"] = [2, False]
    headers2 = HttpHeaders()
    headers2["new"] = "value"
    headers.union(headers2)
    assert headers["new"] == "value"
    assert headers["doesexist"] == "hallo"
    assert headers["thistoo"] == ["a", "b"]


def test_http_request():
    request = HttpRequest("https://journy.io", Method.GET, None, None)

    assert request.url == "https://journy.io"
    assert request.method is Method.GET
    assert request.headers == HttpHeaders()

    assert request.__str__() == "HttpRequest(https://journy.io, Method.GET, {}, None)"

    with pytest.raises(JournyException):
        HttpRequest(123, Method.GET, HttpHeaders(), None)
    with pytest.raises(JournyException):
        HttpRequest("https://journy.io", 123, HttpHeaders(), None)
    with pytest.raises(JournyException):
        HttpRequest("https://journy.io", Method.GET, 123, None)


def test_http_response():
    response = HttpResponse(200, HttpHeaders(), None)

    assert response.status_code == 200
    assert response.headers == HttpHeaders()

    assert response.__str__() == "HttpResponse(200, {}, None)"

    with pytest.raises(JournyException):
        HttpResponse("200", HttpHeaders(), None)
    with pytest.raises(JournyException):
        HttpResponse(200, 213, None)
    with pytest.raises(JournyException):
        HttpResponse(1000, HttpHeaders(), None)


def test_http_client():
    client = HttpClientRequests()

    with pytest.raises(JournyException):
        client.send(123)


def test_http_client_testing():
    dummy_response = HttpResponse(201, HttpHeaders(), {"message": "created"})
    client = HttpClientTesting(dummy_response)

    dummy_request = HttpRequest(
        "/test", Method.POST, HttpHeaders(), {"object": "hello"}
    )
    response = client.send(dummy_request)

    assert response.__str__() == dummy_response.__str__()
    assert client.received_request.__str__() == dummy_request.__str__()

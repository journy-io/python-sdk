from datetime import datetime

import pytest

from sdk.client import Config, Properties, Client
from sdk.events import Event, Metadata
from sdk.httpclient import HttpClientTesting, HttpResponse, HttpHeaders
from sdk.results import Success, TrackingSnippetResponse, ApiKeyDetails, Failure
from sdk.utils import JournyException, APIError


def test_config():
    config = Config("api-key", "https://api.journy.io")

    assert (config.api_key == "api-key")
    assert (config.root_url == "https://api.journy.io")

    assert (config.__str__() == "Config(api-key, https://api.journy.io)")

    with pytest.raises(JournyException):
        Config(123, "https://api.journy.io")
    with pytest.raises(JournyException):
        Config("api-key", 123)


def test_properties():
    properties = Properties()
    assert (properties["doesnotexist"] is None)
    properties["doesexist"] = "hallo"
    assert (properties["doesexist"] == "hallo")
    properties["doesexisttoo"] = 2
    assert (properties["doesexisttoo"] == 2)
    properties["thistoo"] = True
    assert (properties["thistoo"])
    with pytest.raises(JournyException):
        properties[2] = "hallo"
    with pytest.raises(JournyException):
        properties["doesexist"] = [1]
    properties2 = Properties()
    properties2["new"] = "value"
    properties.union(properties2)
    assert (properties["new"] == "value")
    assert (properties["doesexist"] == "hallo")
    assert (properties["thistoo"])


def test_client():
    http_client_testing = HttpClientTesting(HttpResponse())
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)

    assert (client.httpclient.__str__() == http_client_testing.__str__())
    assert (client.config.__str__() == config.__str__())
    assert (
            client.__str__() == "Client(HttpClientTesting(HttpResponse(200, {}, None), None), Config(api-key, https://api.journy.io))")


rate_limit_header = HttpHeaders()
rate_limit_header["X-RateLimit-Remaining"] = "4999"
created_response = HttpResponse(201, rate_limit_header, {"meta": {"requestId": "requestId"}})
too_many_requests_response = HttpResponse(429, rate_limit_header, {"meta": {"requestId": "requestId"}})
tracking_snippet_response = HttpResponse(200, rate_limit_header, {"data": {
    "domain": "journy.io",
    "snippet": "<script>snippet</script>",
},
    "meta": {
        "requestId": "requestId",
    }})
validate_api_key_response = HttpResponse(200, rate_limit_header, {"data": {
    "permissions": [
        "TrackData",
        "GetTrackingSnippet",
        "ReadUserProfile",
    ],
},
    "meta": {
        "requestId": "requestId",
    }})
metadata = Metadata()
metadata["true"] = True
metadata["key"] = "value"
dt = datetime.strptime("2020-11-2 13:37:40", "%Y-%m-%d %H:%M:%S")
event = Event.for_user_in_account("login", "user_id", "account_id").happened_at(dt).with_metadata(metadata)


def test_client_add_event():
    http_client_testing = HttpClientTesting(created_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)
    response = client.add_event(event)

    assert (isinstance(response, Success))
    assert (response.__str__() == "Success(requestId, 4999, None)")
    assert (response.calls_remaining == 4999)
    assert (response.request_id == "requestId")
    assert (response.data is None)

    assert (
            http_client_testing.received_request.__str__() == 'HttpRequest(https://api.journy.io/events, Method.POST, {"content-type": "application/json", "x-api-key": "api-key"}, {"identification": {"userId": "user_id", "accountId": "account_id"}, "name": "login", "triggeredAt": "2020-11-02T13:37:40", "metadata": {"true": true, "key": "value"}})')


def test_client_add_event_with_failure():
    http_client_testing = HttpClientTesting(too_many_requests_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)
    response = client.add_event(event)

    assert (isinstance(response, Failure))
    assert (response.__str__() == "Failure(requestId, 4999, APIError.TooManyRequests)")
    assert (response.calls_remaining == 4999)
    assert (response.request_id == "requestId")
    assert (response.error is APIError.TooManyRequests)

    assert (
            http_client_testing.received_request.__str__() == 'HttpRequest(https://api.journy.io/events, Method.POST, {"content-type": "application/json", "x-api-key": "api-key"}, {"identification": {"userId": "user_id", "accountId": "account_id"}, "name": "login", "triggeredAt": "2020-11-02T13:37:40", "metadata": {"true": true, "key": "value"}})')


def test_client_upsert_user():
    http_client_testing = HttpClientTesting(created_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)
    properties = Properties()

    properties["hasDog"] = False
    properties["name"] = "Manu"

    response = client.upsert_user("manu@journy.io", "userId", properties)

    assert (isinstance(response, Success))
    assert (response.__str__() == "Success(requestId, 4999, None)")
    assert (response.calls_remaining == 4999)
    assert (response.request_id == "requestId")
    assert (response.data is None)

    assert (
            http_client_testing.received_request.__str__() == 'HttpRequest(https://api.journy.io/users/upsert, Method.POST, {"content-type": "application/json", "x-api-key": "api-key"}, {"email": "manu@journy.io", "userId": "userId", "properties": {"hasdog": false, "name": "Manu"}})')


def test_client_upsert_account():
    http_client_testing = HttpClientTesting(created_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)
    properties = Properties()

    properties["haveDog"] = False
    properties["name"] = "Journy"

    response = client.upsert_account("accountId", "journy", properties, ["hansId", "manuId"])

    assert (isinstance(response, Success))
    assert (response.__str__() == "Success(requestId, 4999, None)")
    assert (response.calls_remaining == 4999)
    assert (response.request_id == "requestId")
    assert (response.data is None)

    assert (
            http_client_testing.received_request.__str__() == 'HttpRequest(https://api.journy.io/accounts/upsert, Method.POST, {"content-type": "application/json", "x-api-key": "api-key"}, {"accountId": "accountId", "name": "journy", "properties": {"havedog": false, "name": "Journy"}, "members": ["hansId", "manuId"]})')


def test_client_link():
    http_client_testing = HttpClientTesting(created_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)

    response = client.link("user_id", "device_id")

    assert (isinstance(response, Success))
    assert (response.__str__() == "Success(requestId, 4999, None)")
    assert (response.calls_remaining == 4999)
    assert (response.request_id == "requestId")
    assert (response.data is None)

    assert (
            http_client_testing.received_request.__str__() == 'HttpRequest(https://api.journy.io/link, Method.POST, {"content-type": "application/json", "x-api-key": "api-key"}, {"deviceId": "device_id", "userId": "user_id"})')


def test_client_get_tracking_snippet():
    http_client_testing = HttpClientTesting(tracking_snippet_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)

    response = client.get_tracking_snippet("journy.io")

    assert (isinstance(response, Success))
    assert (
                response.__str__() == "Success(requestId, 4999, TrackingSnippetResponse(journy.io, <script>snippet</script>))")
    assert (response.calls_remaining == 4999)
    assert (response.request_id == "requestId")
    assert (isinstance(response.data, TrackingSnippetResponse))

    assert (
            http_client_testing.received_request.__str__() == 'HttpRequest(https://api.journy.io/tracking/snippet?domain=journy.io, Method.GET, {"content-type": "application/json", "x-api-key": "api-key"}, None)')


def test_client_get_api_key_details():
    http_client_testing = HttpClientTesting(validate_api_key_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)

    response = client.get_api_key_details()

    assert (isinstance(response, Success))
    assert (
            response.__str__() == "Success(requestId, 4999, ApiKeyDetails(['TrackData', 'GetTrackingSnippet', 'ReadUserProfile']))")
    assert (response.calls_remaining == 4999)
    assert (response.request_id == "requestId")
    assert (isinstance(response.data, ApiKeyDetails))

    assert (
            http_client_testing.received_request.__str__() == 'HttpRequest(https://api.journy.io/validate, Method.GET, {"content-type": "application/json", "x-api-key": "api-key"}, None)')

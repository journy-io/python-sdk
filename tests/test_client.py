import pytest
from datetime import datetime

from sdk.client import Config, Properties, Client
from sdk.utils import JournyException
from sdk.httpclient import HttpClientTesting, HttpResponse, HttpHeaders, Method
from sdk.events import Event, Metadata
from sdk.results import Failure, Success, APIError, ApiKeyDetails, TrackingSnippetResponse


def test_config():
    config = Config("api-key", "https://api.journy.io")

    assert (config.api_key == "api-key")
    assert (config.root_url == "https://api.journy.io")

    assert (config.__str__() == "Config(api-key, https://api.journy.io)")

    with pytest.raises(AssertionError):
        Config(123, "https://api.journy.io")
    with pytest.raises(AssertionError):
        Config("api-key", 123)


def test_properties():
    properties = Properties()
    assert (properties["doesnotexist"] is None)
    properties["doesexist"] = "hallo"
    assert (properties["doesexist"] is "hallo")
    properties["doesexisttoo"] = 2
    assert (properties["doesexisttoo"] is 2)
    properties["thistoo"] = True
    assert (properties["thistoo"])
    with pytest.raises(JournyException):
        properties[2] = "hallo"
    with pytest.raises(JournyException):
        properties["doesexist"] = [1]
    properties2 = Properties()
    properties2["new"] = "value"
    properties.union(properties2)
    assert (properties["new"] is "value")
    assert (properties["doesexist"] is "hallo")
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


# TODO: Test failures!

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
    pass


def test_client_get_tracking_snippet():
    pass


def test_client_get_api_key_details():
    pass

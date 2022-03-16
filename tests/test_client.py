from datetime import datetime

import pytest

from journyio.client import Config, Properties, Client
from journyio.events import Event, Metadata
from journyio.httpclient import HttpClientTesting, HttpResponse, HttpHeaders
from journyio.results import Success, TrackingSnippetResponse, ApiKeyDetails, Failure
from journyio.utils import JournyException, APIError
from journyio.user_identified import UserIdentified
from journyio.account_identified import AccountIdentified


def test_config():
    config = Config("api-key", "https://api.journy.io")

    assert config.api_key == "api-key"
    assert config.root_url == "https://api.journy.io"

    assert config.__str__() == "Config(api-key, https://api.journy.io)"

    with pytest.raises(JournyException):
        Config(123, "https://api.journy.io")
    with pytest.raises(JournyException):
        Config("api-key", 123)


def test_properties():
    properties = Properties()
    assert properties["doesnotexist"] is None
    properties["doesexist"] = "hallo"
    assert properties["doesexist"] == "hallo"
    properties["doesexisttoo"] = 2
    assert properties["doesexisttoo"] == 2
    properties["thistoo"] = True
    properties["will_be_deleted"] = None
    properties["array_of_values"] = ["first_value", "second_value"]
    assert properties["thistoo"]
    with pytest.raises(JournyException):
        properties[2] = "hallo"
    with pytest.raises(JournyException):
        properties["doesexist"] = [1]
    properties2 = Properties()
    properties2["new"] = "value"
    properties.union(properties2)
    assert properties["new"] == "value"
    assert properties["doesexist"] == "hallo"
    assert properties["thistoo"]


def test_client():
    http_client_testing = HttpClientTesting(HttpResponse())
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)

    assert client.httpclient.__str__() == http_client_testing.__str__()
    assert client.config.__str__() == config.__str__()
    assert (
        client.__str__()
        == "Client(HttpClientTesting(HttpResponse(200, {}, None), None), Config(api-key, https://api.journy.io))"
    )


rate_limit_header = HttpHeaders()
rate_limit_header["X-RateLimit-Remaining"] = "4999"
created_response = HttpResponse(
    201, rate_limit_header, {"meta": {"requestId": "requestId"}}
)
created_response_202 = HttpResponse(
    202, rate_limit_header, {"meta": {"requestId": "requestId"}}
)
too_many_requests_response = HttpResponse(
    429, rate_limit_header, {"meta": {"requestId": "requestId"}}
)
tracking_snippet_response = HttpResponse(
    200,
    rate_limit_header,
    {
        "data": {
            "domain": "journy.io",
            "snippet": "<script>snippet</script>",
        },
        "meta": {
            "requestId": "requestId",
        },
    },
)
validate_api_key_response = HttpResponse(
    200,
    rate_limit_header,
    {
        "data": {
            "permissions": [
                "TrackData",
                "GetTrackingSnippet",
                "ReadUserProfile",
            ],
        },
        "meta": {
            "requestId": "requestId",
        },
    },
)
metadata = Metadata()
metadata["true"] = True
metadata["key"] = "value"
dt = datetime.strptime("2020-11-2 13:37:40", "%Y-%m-%d %H:%M:%S")
user = UserIdentified("user_id", "user@journy.io")
account = AccountIdentified("account_id", "www.journy.io")
event = (
    Event.for_user_in_account("login", user, account)
    .happened_at(dt)
    .with_metadata(metadata)
)


def test_client_add_event():
    http_client_testing = HttpClientTesting(created_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)
    response = client.add_event(event)

    assert isinstance(response, Success)
    assert response.__str__() == "Success(requestId, 4999, None)"
    assert response.calls_remaining == 4999
    assert response.request_id == "requestId"
    assert response.data is None

    assert (
        http_client_testing.received_request.__str__()
        == 'HttpRequest(https://api.journy.io/track, Method.POST, {"content-type": "application/json", "user-agent": "python-sdk/0.0.0", "x-api-key": "api-key"}, {"identification": {"user": {"email": "user@journy.io", "userId": "user_id"}, "account": {"domain": "www.journy.io", "accountId": "account_id"}}, "name": "login", "metadata": {"true": true, "key": "value"}, "triggeredAt": "2020-11-02T13:37:40"})'
    )


def test_client_add_event_with_failure():
    http_client_testing = HttpClientTesting(too_many_requests_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)
    response = client.add_event(event)

    assert isinstance(response, Failure)
    assert response.__str__() == "Failure(requestId, 4999, APIError.TooManyRequests)"
    assert response.calls_remaining == 4999
    assert response.request_id == "requestId"
    assert response.error is APIError.TooManyRequests

    assert (
        http_client_testing.received_request.__str__()
        == 'HttpRequest(https://api.journy.io/track, Method.POST, {"content-type": "application/json", "user-agent": "python-sdk/0.0.0", "x-api-key": "api-key"}, {"identification": {"user": {"email": "user@journy.io", "userId": "user_id"}, "account": {"domain": "www.journy.io", "accountId": "account_id"}}, "name": "login", "metadata": {"true": true, "key": "value"}, "triggeredAt": "2020-11-02T13:37:40"})'
    )


def test_client_upsert_user():
    http_client_testing = HttpClientTesting(created_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)
    properties = Properties()

    properties["hasDog"] = False
    properties["name"] = "Manu"

    response = client.upsert_user(user, properties)

    assert isinstance(response, Success)
    assert response.__str__() == "Success(requestId, 4999, None)"
    assert response.calls_remaining == 4999
    assert response.request_id == "requestId"
    assert response.data is None

    assert (
        http_client_testing.received_request.__str__()
        == 'HttpRequest(https://api.journy.io/users/upsert, Method.POST, {"content-type": "application/json", "user-agent": "python-sdk/0.0.0", "x-api-key": "api-key"}, {"identification": {"email": "user@journy.io", "userId": "user_id"}, "properties": {"hasdog": false, "name": "Manu"}})'
    )


def test_client_delete_user():
    http_client_testing = HttpClientTesting(created_response_202)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)

    response = client.delete_user(user)

    assert isinstance(response, Success)
    assert response.__str__() == "Success(requestId, 4999, None)"
    assert response.calls_remaining == 4999
    assert response.request_id == "requestId"
    assert response.data is None

    assert (
        http_client_testing.received_request.__str__()
        == 'HttpRequest(https://api.journy.io/users, Method.DELETE, {"content-type": "application/json", "user-agent": "python-sdk/0.0.0", "x-api-key": "api-key"}, {"identification": {"email": "user@journy.io", "userId": "user_id"}})'
    )


def test_client_upsert_account():
    http_client_testing = HttpClientTesting(created_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)
    properties = Properties()

    properties["haveDog"] = False
    properties["name"] = "Journy"

    member1 = UserIdentified.by_user_id("hansId")
    member2 = UserIdentified.by_user_id("manuId")

    response = client.upsert_account(account, properties)

    assert isinstance(response, Success)
    assert response.__str__() == "Success(requestId, 4999, None)"
    assert response.calls_remaining == 4999
    assert response.request_id == "requestId"
    assert response.data is None

    assert (
        http_client_testing.received_request.__str__()
        == 'HttpRequest(https://api.journy.io/accounts/upsert, Method.POST, {"content-type": "application/json", "user-agent": "python-sdk/0.0.0", "x-api-key": "api-key"}, {"identification": {"domain": "www.journy.io", "accountId": "account_id"}, "properties": {"havedog": false, "name": "Journy"}})'
    )


def test_client_delete_account():
    http_client_testing = HttpClientTesting(created_response_202)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)

    response = client.delete_account(account)

    assert isinstance(response, Success)
    assert response.__str__() == "Success(requestId, 4999, None)"
    assert response.calls_remaining == 4999
    assert response.request_id == "requestId"
    assert response.data is None

    assert (
        http_client_testing.received_request.__str__()
        == 'HttpRequest(https://api.journy.io/accounts, Method.DELETE, {"content-type": "application/json", "user-agent": "python-sdk/0.0.0", "x-api-key": "api-key"}, {"identification": {"domain": "www.journy.io", "accountId": "account_id"}})'
    )


def test_client_add_users_to_account():
    http_client_testing = HttpClientTesting(created_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)

    user1 = UserIdentified.by_user_id("hansId")
    user2 = UserIdentified.by_email("manu@journy.io")

    response = client.add_users_to_account(account, [user1, user2])

    assert isinstance(response, Success)
    assert response.__str__() == "Success(requestId, 4999, None)"
    assert response.calls_remaining == 4999
    assert response.request_id == "requestId"
    assert response.data is None

    assert (
        http_client_testing.received_request.__str__()
        == 'HttpRequest(https://api.journy.io/accounts/users/add, Method.POST, {"content-type": "application/json", "user-agent": "python-sdk/0.0.0", "x-api-key": "api-key"}, {"account": {"domain": "www.journy.io", "accountId": "account_id"}, "users": [{"identification": {"userId": "hansId"}}, {"identification": {"email": "manu@journy.io"}}]})'
    )


def test_client_remove_users_from_account():
    http_client_testing = HttpClientTesting(created_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)

    user1 = UserIdentified.by_user_id("hansId")
    user2 = UserIdentified.by_email("manu@journy.io")

    response = client.remove_users_from_account(account, [user1, user2])

    assert isinstance(response, Success)
    assert response.__str__() == "Success(requestId, 4999, None)"
    assert response.calls_remaining == 4999
    assert response.request_id == "requestId"
    assert response.data is None

    assert (
        http_client_testing.received_request.__str__()
        == 'HttpRequest(https://api.journy.io/accounts/users/remove, Method.POST, {"content-type": "application/json", "user-agent": "python-sdk/0.0.0", "x-api-key": "api-key"}, {"account": {"domain": "www.journy.io", "accountId": "account_id"}, "users": [{"identification": {"userId": "hansId"}}, {"identification": {"email": "manu@journy.io"}}]})'
    )


def test_client_link():
    http_client_testing = HttpClientTesting(created_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)

    response = client.link(user, "device_id")

    assert isinstance(response, Success)
    assert response.__str__() == "Success(requestId, 4999, None)"
    assert response.calls_remaining == 4999
    assert response.request_id == "requestId"
    assert response.data is None

    assert (
        http_client_testing.received_request.__str__()
        == 'HttpRequest(https://api.journy.io/link, Method.POST, {"content-type": "application/json", "user-agent": "python-sdk/0.0.0", "x-api-key": "api-key"}, {"deviceId": "device_id", "identification": {"email": "user@journy.io", "userId": "user_id"}})'
    )


def test_client_get_tracking_snippet():
    http_client_testing = HttpClientTesting(tracking_snippet_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)

    response = client.get_tracking_snippet("journy.io")

    assert isinstance(response, Success)
    assert (
        response.__str__()
        == "Success(requestId, 4999, TrackingSnippetResponse(journy.io, <script>snippet</script>))"
    )
    assert response.calls_remaining == 4999
    assert response.request_id == "requestId"
    assert isinstance(response.data, TrackingSnippetResponse)

    assert (
        http_client_testing.received_request.__str__()
        == 'HttpRequest(https://api.journy.io/tracking/snippet?domain=journy.io, Method.GET, {"content-type": "application/json", "user-agent": "python-sdk/0.0.0", "x-api-key": "api-key"}, None)'
    )


def test_client_get_api_key_details():
    http_client_testing = HttpClientTesting(validate_api_key_response)
    config = Config("api-key", "https://api.journy.io")

    client = Client(http_client_testing, config)

    response = client.get_api_key_details()

    assert isinstance(response, Success)
    assert (
        response.__str__()
        == "Success(requestId, 4999, ApiKeyDetails(['TrackData', 'GetTrackingSnippet', 'ReadUserProfile']))"
    )
    assert response.calls_remaining == 4999
    assert response.request_id == "requestId"
    assert isinstance(response.data, ApiKeyDetails)

    assert (
        http_client_testing.received_request.__str__()
        == 'HttpRequest(https://api.journy.io/validate, Method.GET, {"content-type": "application/json", "user-agent": "python-sdk/0.0.0", "x-api-key": "api-key"}, None)'
    )

import json
from collections import defaultdict
from datetime import datetime
from urllib import parse

from typing import List

from .events import Event
from .httpclient import HttpRequest, Method, HttpClient, HttpResponse, HttpHeaders
from .results import Failure, Success, ApiKeyDetails, TrackingSnippetResponse
from .utils import JournyException, status_code_to_api_error, assert_journy
from .user_identified import UserIdentified
from .account_identified import AccountIdentified
from .version import version


class Properties(dict):
    def __init__(self):
        super().__init__()
        self.properties = defaultdict(lambda _: None)

    def __getitem__(self, key: str):
        assert_journy(isinstance(key, str), "The key is not a string.")
        return self.properties.get(key.lower().strip())

    def __setitem__(
        self, key: str, value: str or List[str] or bool or int or datetime or None
    ):
        assert_journy(isinstance(key, str), "The key is not a string.")
        if (
            isinstance(value, str)
            or isinstance(value, int)
            or isinstance(value, bool)
            or isinstance(value, datetime)
            or value is None
            or (isinstance(value, list) and all([isinstance(el, str) for el in value]))
        ):
            if isinstance(value, datetime):
                value = str(value.isoformat())
            self.properties.__setitem__(key.lower().strip(), value)
        else:
            raise JournyException(
                "Value is not a string, number, boolean, datetime or None."
            )

    def union(self, other):
        self.properties.update(other.properties)
        return self

    def __str__(self):
        return json.dumps(self.properties)

    def __repr__(self):
        return self.__str__()


class Config(object):
    """
    A config for the Journy.io's python journyio client.
    This contains all the necessary information for the client to work properly.
    """

    def __init__(self, api_key: str, root_url: str or None = "https://api.journy.io"):
        if root_url is None:
            root_url = "https://api.journy.io"
        assert_journy(isinstance(api_key, str), "The api key is not a string.")
        assert_journy(isinstance(root_url, str), "The root url is not a string.")

        self.api_key = api_key
        self.root_url = root_url

    def __repr__(self):
        return f"Config({self.api_key}, {self.root_url})"

    def __str__(self):
        return self.__repr__()


class Client(object):
    """
    Journy.io's python journyio client.
    """

    def __init__(self, httpclient: HttpClient, config: Config):
        assert_journy(
            isinstance(httpclient, HttpClient),
            "The httpClient is not a HttpClient object.",
        )
        assert_journy(isinstance(config, Config), "The config is not a Config object.")

        self.httpclient = httpclient
        self.config = config

    def __repr__(self):
        return f"Client({self.httpclient}, {self.config})"

    def __str__(self):
        return self.__repr__()

    def __create_url(self, path) -> str:
        return self.config.root_url + path

    def __get_headers(self) -> HttpHeaders:
        headers = HttpHeaders()
        headers["Content-Type"] = "application/json"
        headers["User-Agent"] = f"python-sdk/{version}"
        headers["x-api-key"] = self.config.api_key
        return headers

    @staticmethod
    def __parse_calls_remaining(response: HttpResponse) -> int:
        remaining = response.headers["X-RateLimit-Remaining"]
        try:
            return int(remaining)
        except ValueError:
            return None

    def add_event(self, event: Event) -> Success[None] or Failure:
        assert_journy(isinstance(event, Event), "The event should be an Event object.")

        try:
            body = {
                "identification": {},
                "name": event.name,
                "metadata": event.metadata.metadata,
            }
            if event.date:
                body["triggeredAt"] = event.date.isoformat()
            if event.user:
                body["identification"]["user"] = event.user.format_identification()
            if event.account:
                body["identification"][
                    "account"
                ] = event.account.format_identification()

            request = HttpRequest(
                self.__create_url("/track"),
                Method.POST,
                self.__get_headers(),
                json.dumps(body),
            )
            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)
            if not (200 <= response.status_code < 300):
                return Failure(
                    response.body["meta"]["requestId"],
                    calls_remaining,
                    status_code_to_api_error(response.status_code),
                )
            return Success[None](
                response.body["meta"]["requestId"], calls_remaining, None
            )
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

    def upsert_user(
        self, user: UserIdentified, properties: Properties
    ) -> Success[None] or Failure:
        assert_journy(
            isinstance(user, UserIdentified), "User is not a UserIdentified object."
        )
        assert_journy(
            isinstance(properties, Properties), "Properties is not a Properties object."
        )

        try:
            request = HttpRequest(
                self.__create_url("/users/upsert"),
                Method.POST,
                self.__get_headers(),
                json.dumps(
                    {
                        "identification": user.format_identification(),
                        "properties": properties.properties,
                    }
                ),
            )
            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)
            if not (200 <= response.status_code < 300):
                return Failure(
                    response.body["meta"]["requestId"],
                    calls_remaining,
                    status_code_to_api_error(response.status_code),
                )
            return Success[None](
                response.body["meta"]["requestId"], calls_remaining, None
            )
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

    def delete_user(self, user: UserIdentified) -> Success[None] or Failure:
        assert_journy(
            isinstance(user, UserIdentified), "User is not a UserIdentified object."
        )

        try:
            request = HttpRequest(
                self.__create_url("/users"),
                Method.DELETE,
                self.__get_headers(),
                json.dumps({"identification": user.format_identification()}),
            )
            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)
            if not (200 <= response.status_code < 300):
                return Failure(
                    response.body["meta"]["requestId"],
                    calls_remaining,
                    status_code_to_api_error(response.status_code),
                )
            return Success[None](
                response.body["meta"]["requestId"], calls_remaining, None
            )
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

    def upsert_account(
        self, account: AccountIdentified, properties: Properties or None
    ) -> Success[None] or Failure:
        assert_journy(
            isinstance(account, AccountIdentified),
            "Account is not an AccountIdentified object.",
        )
        if properties is not None:
            assert_journy(
                isinstance(properties, Properties),
                "Properties is not a Properties object.",
            )

        try:
            request = HttpRequest(
                self.__create_url("/accounts/upsert"),
                Method.POST,
                self.__get_headers(),
                json.dumps(
                    {
                        "identification": account.format_identification(),
                        "properties": properties.properties,
                    }
                ),
            )
            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)
            if not (200 <= response.status_code < 300):
                return Failure(
                    response.body["meta"]["requestId"],
                    calls_remaining,
                    status_code_to_api_error(response.status_code),
                )
            return Success[None](
                response.body["meta"]["requestId"], calls_remaining, None
            )
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

    def delete_account(self, account: AccountIdentified) -> Success[None] or Failure:
        assert_journy(
            isinstance(account, AccountIdentified),
            "Account is not an AccountIdentified object.",
        )

        try:
            request = HttpRequest(
                self.__create_url("/accounts"),
                Method.DELETE,
                self.__get_headers(),
                json.dumps(
                    {
                        "identification": account.format_identification(),
                    }
                ),
            )
            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)
            if not (200 <= response.status_code < 300):
                return Failure(
                    response.body["meta"]["requestId"],
                    calls_remaining,
                    status_code_to_api_error(response.status_code),
                )
            return Success[None](
                response.body["meta"]["requestId"], calls_remaining, None
            )
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

    def add_users_to_account(
        self, account: AccountIdentified, users: List[UserIdentified]
    ) -> Success[None] or Failure:
        assert_journy(
            isinstance(account, AccountIdentified),
            "Account is not an AccountIdentified object.",
        )
        for user in users:
            assert_journy(
                isinstance(user, UserIdentified),
                f"User {user} is not a UserIdentified object.",
            )

        try:
            request = HttpRequest(
                self.__create_url("/accounts/users/add"),
                Method.POST,
                self.__get_headers(),
                json.dumps(
                    {
                        "account": account.format_identification(),
                        "users": [
                            {"identification": user.format_identification()}
                            for user in users
                        ],
                    }
                ),
            )
            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)
            if not (200 <= response.status_code < 300):
                return Failure(
                    response.body["meta"]["requestId"],
                    calls_remaining,
                    status_code_to_api_error(response.status_code),
                )
            return Success[None](
                response.body["meta"]["requestId"], calls_remaining, None
            )
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

    def remove_users_from_account(
        self, account: AccountIdentified, users: List[UserIdentified]
    ) -> Success[None] or Failure:
        assert_journy(
            isinstance(account, AccountIdentified),
            "Account is not an AccountIdentified object.",
        )
        for user in users:
            assert_journy(
                isinstance(user, UserIdentified),
                f"User {user} is not a UserIdentified object.",
            )

        try:
            request = HttpRequest(
                self.__create_url("/accounts/users/remove"),
                Method.POST,
                self.__get_headers(),
                json.dumps(
                    {
                        "account": account.format_identification(),
                        "users": [
                            {"identification": user.format_identification()}
                            for user in users
                        ],
                    }
                ),
            )
            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)
            if not (200 <= response.status_code < 300):
                return Failure(
                    response.body["meta"]["requestId"],
                    calls_remaining,
                    status_code_to_api_error(response.status_code),
                )
            return Success[None](
                response.body["meta"]["requestId"], calls_remaining, None
            )
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

    def link(self, user: UserIdentified, device_id: str) -> Success[None] or Failure:
        assert_journy(
            isinstance(user, UserIdentified), "The user is not a UserIdentified object."
        )
        assert_journy(isinstance(device_id, str), "The device id is not a string.")

        try:
            request = HttpRequest(
                self.__create_url("/link"),
                Method.POST,
                self.__get_headers(),
                json.dumps(
                    {
                        "deviceId": device_id,
                        "identification": user.format_identification(),
                    }
                ),
            )
            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)

            if not (200 <= response.status_code < 300):
                return Failure(
                    response.body["meta"]["requestId"],
                    calls_remaining,
                    status_code_to_api_error(response.status_code),
                )
            return Success[None](
                response.body["meta"]["requestId"], calls_remaining, None
            )
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

    def get_tracking_snippet(
        self, domain: str
    ) -> Success[TrackingSnippetResponse] or Failure:
        assert_journy(isinstance(domain, str), "domain should be a string.")

        try:
            request = HttpRequest(
                self.__create_url(
                    "/tracking/snippet?domain={}".format(parse.quote_plus(domain))
                ),
                Method.GET,
                self.__get_headers(),
                None,
            )
            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)

            if not (200 <= response.status_code < 300):
                return Failure(
                    response.body["meta"]["requestId"],
                    calls_remaining,
                    status_code_to_api_error(response.status_code),
                )
            return Success[TrackingSnippetResponse](
                response.body["meta"]["requestId"],
                calls_remaining,
                TrackingSnippetResponse(
                    response.body["data"]["domain"], response.body["data"]["snippet"]
                ),
            )
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

    def get_api_key_details(self) -> Success[ApiKeyDetails] or Failure:
        try:
            request = HttpRequest(
                self.__create_url("/validate"), Method.GET, self.__get_headers(), None
            )
            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)

            if not (200 <= response.status_code < 300):
                return Failure(
                    response.body["meta"]["requestId"],
                    calls_remaining,
                    status_code_to_api_error(response.status_code),
                )
            return Success[ApiKeyDetails](
                response.body["meta"]["requestId"],
                calls_remaining,
                ApiKeyDetails(response.body["data"]["permissions"]),
            )
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

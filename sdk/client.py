from collections import defaultdict
from datetime import datetime

from .httpclient import HttpRequest, Method, HttpClient, HttpResponse
from .utils import JournyException, status_code_to_api_error, assert_journy
from .results import Failure, Success, ApiKeyDetails, LinkResponse, TrackingSnippetResponse
from .events import Event


class Properties(dict):

    def __init__(self):
        super().__init__()
        self.headers = defaultdict(lambda _: None)

    def __getitem__(self, key: str):
        assert_journy(isinstance(key, str), "The key is not a string.")

        return self.headers.get(key.lower().strip())

    def __setitem__(self, key: str, value: str or list):
        assert_journy(isinstance(key, str), "The key is not a string.")

        if isinstance(value, str) or isinstance(value, int) or isinstance(value, bool) or isinstance(value, datetime):
            self.headers.__setitem__(key.lower().strip(), value)
        else:
            raise JournyException("Value is not a string, number, boolean or datetime.")


class Config(object):
    """
    A config for the Journy.io's python sdk client.
    This contains all the necessary information for the client to work properly.
    """

    def __init__(self, api_key: str, root_url: str or None = "https://api.journy.io"):
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
    Journy.io's python sdk client.
    """

    def __init__(self, httpclient: HttpClient, config: Config):
        assert_journy(isinstance(httpclient, HttpClient), "The httpClient is not a HttpClient object.")
        assert_journy(isinstance(config, Config), "The config is not a Config object.")

        self.httpclient = httpclient
        self.config = config

    def __repr__(self):
        return f"Client({self.httpclient}, {self.config})"

    def __str__(self):
        return self.__repr__()

    def __create_url(self, path):
        return self.config.root_url + path

    def __get_headers(self):
        return {"x-api-key": self.config.api_key, "Content-Type": "application/json"}

    @staticmethod
    def __parse_calls_remaining(response: HttpResponse):
        remaining = response.headers["X-RateLimit-Remaining"]
        try:
            return int(remaining)
        except ValueError:
            return None

    def add_event(self, event: Event):
        try:
            request = HttpRequest(self.__create_url("/events"), Method.POST,
                                  {**self.__get_headers()},
                                  {
                                      "identification": {
                                          "userId": event.user_id,
                                          "accountId": event.account_id
                                      },
                                      "name": event.name,
                                      "triggeredAt": event.date.isoformat() if event.date else None,
                                      "metadata": event.metadata
                                  })
            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)
            if not (200 <= response.status_code < 300):
                return Failure(response.data.meta.requestId, calls_remaining,
                               status_code_to_api_error(response.status_code))
            return Success[None](response.data.meta.requestId, calls_remaining, None)
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

    def upsert_user(self, email: str, user_id: str, properties: Properties):
        assert_journy(isinstance(email, str), "The email is not a string.")
        assert_journy(isinstance(user_id, str), "The user id is not a string.")
        assert_journy(isinstance(properties, Properties), "Properties is not a Properties object.")

        try:
            request = HttpRequest(self.__create_url("/users/upsert"), Method.POST,
                                  {**self.__get_headers()},
                                  {
                                      "email": email,
                                      "userId": user_id,
                                      "properties": properties
                                  })
            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)
            if not (200 <= response.status_code < 300):
                return Failure(response.data.meta.requestId, calls_remaining,
                               status_code_to_api_error(response.status_code))
            return Success[None](response.data.meta.requestId, calls_remaining, None)
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

    def upsert_account(self, account_id, name, properties, members):
        assert_journy(isinstance(account_id, str), "The account id is not a string.")
        assert_journy(isinstance(name, str), "The name is not a string.")
        assert_journy(isinstance(properties, Properties), "Properties is not a Properties object.")

        for member in members:
            assert_journy(isinstance(member, str), f"Member {member} is not a string.")

        try:
            request = HttpRequest(self.__create_url("/users/upsert"), Method.POST,
                                  {**self.__get_headers()},
                                  {
                                      "accountId": account_id,
                                      "name": name,
                                      "properties": properties,
                                      "members": members
                                  })
            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)
            if not (200 <= response.status_code < 300):
                return Failure(response.data.meta.requestId, calls_remaining,
                               status_code_to_api_error(response.status_code))
            return Success[None](response.data.meta.requestId, calls_remaining, None)
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

    def link(self, user_id: str, device_id: str) -> Success[LinkResponse] or Failure:
        assert (isinstance(user_id, str))
        assert (isinstance(device_id, str))
        assert_journy(isinstance(user_id, str), "The user id is not a string.")
        assert_journy(isinstance(device_id, str), "The device id is not a string.")

        try:
            request = HttpRequest(self.__create_url("/link"), Method.POST,
                                  {**self.__get_headers()}, {
                                      "deviceId": device_id,
                                      "userId": user_id
                                  })

            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)

            if not (200 <= response.status_code < 300):
                return Failure(response.data.meta.requestId, calls_remaining,
                               status_code_to_api_error(response.status_code))
            return Success[LinkResponse](response.data.meta.requestId, calls_remaining,
                                         LinkResponse(response.data.message))
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

    def get_tracking_snippet(self) -> Success[TrackingSnippetResponse] or Failure:
        try:
            request = HttpRequest(self.__create_url("/tracking/snippet"), Method.GET,
                                  {**self.__get_headers()})

            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)

            if not (200 <= response.status_code < 300):
                return Failure(response.data.meta.requestId, calls_remaining,
                               status_code_to_api_error(response.status_code))
            return Success[TrackingSnippetResponse](response.data.meta.requestId, calls_remaining,
                                                    TrackingSnippetResponse(response.data.data.domain,
                                                                            response.data.data.snippet))
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

    def get_api_key_details(self) -> Success[ApiKeyDetails] or Failure:
        try:
            request = HttpRequest(self.__create_url("/validate"), Method.GET,
                                  {**self.__get_headers()})
            response = self.httpclient.send(request)
            calls_remaining = Client.__parse_calls_remaining(response)
            if not (200 <= response.status_code < 300):
                return Failure(response.data.meta.requestId, calls_remaining,
                               status_code_to_api_error(response.status_code))
            return Success[ApiKeyDetails](response.data.meta.requestId, calls_remaining,
                                          ApiKeyDetails(response.data.data.permissions))
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

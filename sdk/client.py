from .httpclient import HttpRequest, Method, HttpClient
from .utils import JournyException, status_code_to_api_error
from .results import Failure, Success, ApiKeyDetails


class Config(object):
    """
    A config for the Journy.io's python sdk client.
    This contains all the necessary information for the client to work properly.
    """

    def __init__(self, api_key: str, root_url: str or None = "https://api.journy.io"):
        assert (isinstance(api_key, str))
        assert (isinstance(root_url, str))

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
        assert (isinstance(httpclient, HttpClient))
        assert (isinstance(config, Config))

        self.httpclient = httpclient
        self.config = config

    def __repr__(self):
        return f"Client({self.httpclient}, {self.config})"

    def __str__(self):
        return self.__repr__()

    def __create_url(self, path):
        return self.config.root_url + path

    def __get_headers(self):
        return {"x-api-key": self.config.api_key}

    def add_event(self, event):
        pass

    def upsert_user(self, args):
        pass

    def upsert_account(self, args):
        pass

    def link(self, args):
        pass

    def get_tracking_snippet(self, args):
        pass

    def get_api_key_details(self) -> Success[ApiKeyDetails] or Failure:
        try:
            request = HttpRequest(self.__create_url("/validate"), Method.GET,
                                  {**self.__get_headers(), "Content-Type": "application/json"})
            response = self.httpclient.send(request)
            if not (200 <= response.status_code <= 299):
                return Failure(response.data.meta.requestId, response.data.meta.callsRemaining,
                               status_code_to_api_error(response.status_code))
            return Success[ApiKeyDetails](response.data.meta.requestId, response.data.meta.callsRemaining,
                                          ApiKeyDetails(response.data.data.permissions))
        except JournyException as e:
            raise e
        except Exception:
            raise JournyException(f"An unknown error has occurred")

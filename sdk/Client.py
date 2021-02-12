class Config(object):
    def __init__(self, api_key, root_url="https://api.journy.io"):
        self.api_key = api_key
        self.root_url = root_url

    def __repr__(self):
        return f"Config({self.api_key}, {self.root_url})"

    def __str__(self):
        return self.__repr__()


class Client(object):
    """
    journy.io sdk
    """

    def __init__(self, http_client, config):
        self.http_client = http_client
        self.config = config

    def __repr__(self):
        return f"Client({self.http_client}, {self.config})"

    def __str__(self):
        return self.__repr__()

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

    def get_api_key_details(self, args):
        pass

from .utils import JournyException
from collections import defaultdict


class Metadata(dict):
    def __init__(self):
        super().__init__()
        self.headers = defaultdict(lambda _: None)

    def __getitem__(self, key: str):
        if not isinstance(key, str):
            raise JournyException("The key is not a string.")
        return self.headers.get(key.lower().strip())

    def __setitem__(self, key: str, value: str or bool or int):
        if not isinstance(key, str):
            raise JournyException("The key is not a string.")
        if isinstance(value, str) or isinstance(value, int) or isinstance(value, bool):
            self.headers.__setitem__(key.lower().strip(), value)  # TODO: thoroughly test this!
        else:
            raise JournyException("Value is not a string, number or boolean.")

    def union(self, metadata):
        self.headers.update(metadata.headers)
        return self


class Event(object):
    """
    TODO: Some usage examples (of static method and happened_at, with_metadata)
    TODO: Warning to not initialise without static methods
    """

    def __init__(self, name: str, user_id: str or None, account_id: str or None, date: str or None,
                 metadata: Metadata):
        if not name:
            raise JournyException("Event name cannot be empty!")

        assert (isinstance(name, str))
        if user_id:
            assert (isinstance(user_id, str))
        if account_id:
            assert (isinstance(account_id, str))
        if date:
            assert (isinstance(date, str))
        assert (isinstance(metadata, Metadata))

        self.name = name
        self.user_id = user_id
        self.account_id = account_id
        self.date = date
        self.metadata = metadata

    def happened_at(self, date: str):
        return Event(self.name, self.user_id, self.account_id, date, self.metadata)

    def with_metadata(self, metadata: Metadata):
        return Event(self.name, self.user_id, self.account_id, self.date, self.metadata.union(metadata))

    @staticmethod
    def for_user(name: str, user_id: str):
        if not user_id:
            raise JournyException("user_id can not be empty!")
        return Event(name, user_id, None, None, Metadata())

    @staticmethod
    def for_account(name: str, account_id: str):
        if not account_id:
            raise JournyException("account_id can not be empty!")
        return Event(name, None, account_id, None, Metadata())

    @staticmethod
    def for_user_in_account(name: str, user_id: str, account_id: str):
        if not account_id or not user_id:
            raise JournyException("user_id and account_id can not be empty!")
        return Event(name, user_id, account_id, None, Metadata())

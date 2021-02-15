import datetime
import json
from collections import defaultdict

from .utils import JournyException, assert_journy


class Metadata(dict):

    def __init__(self):
        super().__init__()
        self.metadata = defaultdict(lambda _: None)

    def __getitem__(self, key: str):
        assert_journy(isinstance(key, str), "The key is not a string.")

        return self.metadata.get(key.lower().strip())

    def __setitem__(self, key: str, value: str or bool or int):
        assert_journy(isinstance(key, str), "The key is not a string.")

        if isinstance(value, str) or isinstance(value, int) or isinstance(value, bool):
            self.metadata.__setitem__(key.lower().strip(), value)
        else:
            raise JournyException("Value is not a string, number or boolean.")

    def union(self, metadata):
        self.metadata.update(metadata.metadata)
        return self

    def __str__(self):
        return json.dumps(self.metadata)

    def __repr__(self):
        return self.__str__()


class Event(object):
    """
    Warning: please do create Event objects via the static methods (for_user, for_account, for_user_in_account) and not
    via the constructor. Not doing using them could lead to problems.
    """

    def __init__(self, name: str, user_id: str or None, account_id: str or None, date: str or None,
                 metadata: Metadata):
        assert_journy(name, "Event name cannot be empty.")
        assert_journy(isinstance(name, str), "The name is not a string.")

        if user_id:
            assert_journy(isinstance(user_id, str), "The user id is not a string.")
        if account_id:
            assert_journy(isinstance(account_id, str), "The account id is not a string.")
        if date:
            assert_journy(isinstance(date, datetime.datetime), "The date is not a datetime object.")

        assert_journy(isinstance(metadata, Metadata), "The metadata should be a Metadata object")

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
        assert_journy(user_id, "user_id can not be empty!")
        return Event(name, user_id, None, None, Metadata())

    @staticmethod
    def for_account(name: str, account_id: str):
        assert_journy(account_id, "account_id can not be empty!")
        return Event(name, None, account_id, None, Metadata())

    @staticmethod
    def for_user_in_account(name: str, user_id: str, account_id: str):
        assert_journy(account_id and user_id, "user_id and account_id can not be empty!")
        return Event(name, user_id, account_id, None, Metadata())

    def __str__(self):
        return f"Event({self.name}, {self.user_id}, {self.account_id}, {self.date}, {self.metadata})"

    def __repr__(self):
        return self.__str__()

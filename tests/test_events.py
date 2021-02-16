from datetime import datetime

import pytest

from journyio.events import Metadata, Event
from journyio.utils import JournyException


def test_metadata():
    metadata = Metadata()
    assert (metadata["doesnotexist"] is None)
    metadata["doesexist"] = "hallo"
    assert (metadata["doesexist"] == "hallo")
    metadata["doesexisttoo"] = 2
    assert (metadata["doesexisttoo"] == 2)
    metadata["thistoo"] = True
    assert (metadata["thistoo"])
    with pytest.raises(JournyException):
        metadata[2] = "hallo"
    with pytest.raises(JournyException):
        metadata["doesexist"] = [1]
    metadata2 = Metadata()
    metadata2["new"] = "value"
    metadata.union(metadata2)
    assert (metadata2["new"] == "value")
    assert (metadata["doesexist"] == "hallo")
    assert (metadata["thistoo"])


def test_event():
    metadata = Metadata()
    metadata["true"] = True
    metadata["key"] = "value"

    dt = datetime.strptime("2020-11-2 13:37:40", "%Y-%m-%d %H:%M:%S")
    dt2 = datetime.strptime("2020-11-2 13:37:50", "%Y-%m-%d %H:%M:%S")
    event_1 = Event.for_user("login", "user_id").happened_at(dt)
    event_2 = Event.for_user("logout", "user_id").happened_at(dt2)
    event_3 = Event.for_account("login", "account_id").happened_at(dt)
    event_4 = Event.for_user_in_account("login", "user_id", "account_id").happened_at(dt2).with_metadata(metadata)

    assert (event_1.__str__() == "Event(login, user_id, None, 2020-11-02 13:37:40, {})")
    assert (event_2.__str__() == "Event(logout, user_id, None, 2020-11-02 13:37:50, {})")
    assert (event_3.__str__() == "Event(login, None, account_id, 2020-11-02 13:37:40, {})")
    assert (
        event_4.__str__() == 'Event(login, user_id, account_id, 2020-11-02 13:37:50, {"true": true, "key": "value"})')

    with pytest.raises(JournyException):
        Event(None, None, None, None, Metadata())

    with pytest.raises(JournyException):
        Event("login", 1234, 1234, None, Metadata())

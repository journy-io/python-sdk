import pytest

from journyio.user_identified import UserIdentified
from journyio.utils import JournyException


def test_user_identified():
    user1 = UserIdentified("user_id", "email")
    user2 = UserIdentified.by_user_id("user_id")
    user3 = UserIdentified.by_email("email")

    assert user1.format_identification() == {"email": "email", "userId": "user_id"}
    assert user2.format_identification() == {"userId": "user_id"}
    assert user3.format_identification() == {"email": "email"}

    with pytest.raises(JournyException):
        UserIdentified("", "")
    with pytest.raises(JournyException):
        UserIdentified(None, None)
    with pytest.raises(JournyException):
        UserIdentified.by_user_id(None)
    with pytest.raises(JournyException):
        UserIdentified.by_email(None)

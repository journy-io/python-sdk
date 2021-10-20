import pytest

from journyio.account_identified import AccountIdentified
from journyio.utils import JournyException


def test_user_identified():
    user1 = AccountIdentified("account_id", "domain")
    user2 = AccountIdentified.by_account_id("account_id")
    user3 = AccountIdentified.by_domain("domain")

    assert user1.format_identification() == {
        "accountId": "account_id",
        "domain": "domain",
    }
    assert user2.format_identification() == {"accountId": "account_id"}
    assert user3.format_identification() == {"domain": "domain"}

    with pytest.raises(JournyException):
        AccountIdentified("", "")
    with pytest.raises(JournyException):
        AccountIdentified(None, None)
    with pytest.raises(JournyException):
        AccountIdentified.by_domain(None)
    with pytest.raises(JournyException):
        AccountIdentified.by_account_id(None)

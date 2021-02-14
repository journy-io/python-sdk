import pytest

from sdk.client import Config, Properties
from sdk.utils import JournyException

def test_config():
    config = Config("api-key", "https://api.journy.io")

    assert (config.api_key == "api-key")
    assert (config.root_url == "https://api.journy.io")

    assert (config.__str__() == "Config(api-key, https://api.journy.io)")

    with pytest.raises(AssertionError):
        Config(123, "https://api.journy.io")
    with pytest.raises(AssertionError):
        Config("api-key", 123)


def test_properties():
    properties = Properties()
    assert (properties["doesnotexist"] is None)
    properties["doesexist"] = "hallo"
    assert (properties["doesexist"] is "hallo")
    properties["doesexisttoo"] = 2
    assert (properties["doesexisttoo"] is 2)
    properties["thistoo"] = True
    assert (properties["thistoo"])
    with pytest.raises(JournyException):
        properties[2] = "hallo"
    with pytest.raises(JournyException):
        properties["doesexist"] = [1]
    properties2 = Properties()
    properties2["new"] = "value"
    properties.union(properties2)
    assert (properties["new"] is "value")
    assert (properties["doesexist"] is "hallo")
    assert (properties["thistoo"])


def test_client():
    pass  # TODO

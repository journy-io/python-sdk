import pytest

from sdk.client import Config


def test_config():
    config = Config("api-key", "https://api.journy.io")

    assert (config.api_key == "api-key")
    assert (config.root_url == "https://api.journy.io")

    assert (config.__str__() == "Config(api-key, https://api.journy.io)")

    with pytest.raises(AssertionError):
        Config(123, "https://api.journy.io")
    with pytest.raises(AssertionError):
        Config("api-key", 123)


def test_client():
    pass  # TODO

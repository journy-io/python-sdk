import pytest

from sdk.results import APIError
from sdk.utils import JournyException, status_code_to_api_error


def test_journy_exception():
    with pytest.raises(JournyException):
        raise JournyException("custom message")

    try:
        raise JournyException("custom message")
    except JournyException as e:
        assert (e.__str__() == "JournyException(custom message)")


def test_status_code_to_api_error():
    with pytest.raises(AssertionError):
        raise status_code_to_api_error("status_code")

    assert (status_code_to_api_error(200) is APIError.UnknownError)
    assert (status_code_to_api_error(401) is APIError.UnauthorizedError)
    assert (status_code_to_api_error(400) is APIError.BadArgumentsError)
    assert (status_code_to_api_error(429) is APIError.TooManyRequests)
    assert (status_code_to_api_error(404) is APIError.NotFoundError)
    assert (status_code_to_api_error(500) is APIError.ServerError)
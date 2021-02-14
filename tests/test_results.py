import pytest

from sdk.results import Success, Failure, TrackingSnippetResponse, ApiKeyDetails, APIError


def test_success():
    success = Success[None]("request_id", 100, None)
    assert (success.data is None)
    assert (success.request_id == "request_id")
    assert (success.calls_remaining == 100)

    with pytest.raises(AssertionError):
        Success[None](1234, 100, None)

    with pytest.raises(AssertionError):
        Success[None]("request_id", "100", None)

    assert (success.__str__() == "Success(request_id, 100, None)")


def test_failure():
    failure = Failure(None, None, APIError.ServerError)
    failure2 = Failure("request_id", 100, APIError.UnknownError)

    assert (failure2.request_id == "request_id")
    assert (failure2.calls_remaining == 100)
    assert (failure2.error is APIError.UnknownError)
    assert (failure.__str__() == "Error(None, None, APIError.ServerError)")
    assert (failure2.__str__() == "Error(request_id, 100, APIError.UnknownError)")

    with pytest.raises(AssertionError):
        Failure("request_id", "100", APIError.ServerError)
    with pytest.raises(AssertionError):
        Failure(100, 100, APIError.ServerError)
    with pytest.raises(AssertionError):
        Failure("request_id", 100, None)


def test_tracking_snippet_response():
    response = TrackingSnippetResponse("www.journy.io", "<div>SNIPPET</div>")

    assert (response.domain == "www.journy.io")
    assert (response.snippet == "<div>SNIPPET</div>")

    assert (response.__str__() == "TrackingSnippetResponse(www.journy.io, <div>SNIPPET</div>)")

    with pytest.raises(AssertionError):
        TrackingSnippetResponse(123, "snippet")
    with pytest.raises(AssertionError):
        TrackingSnippetResponse("domain", 123)

    success = Success[TrackingSnippetResponse]("request_id", 100, response)

    assert (success.data.__str__() == response.__str__())


def test_api_key_details():
    details = ApiKeyDetails(["TrackData", "GetTrackingSnippet"])

    assert (details.permissions == ["TrackData", "GetTrackingSnippet"])

    assert (details.__str__() == "ApiKeyDetails(['TrackData', 'GetTrackingSnippet'])")

    with pytest.raises(AssertionError):
        ApiKeyDetails(123)

    success = Success[ApiKeyDetails]("request_id", 100, details)

    assert (success.data.__str__() == details.__str__())

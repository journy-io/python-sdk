[![journy.io](https://raw.githubusercontent.com/journy-io/python-sdk/main/banner.png?token=AIYSKXPKLRTOT3S4HQDXE2DAGPNL4)](https://journy.io/?utm_source=github&utm_content=readme-python-sdk)

# journy.io Python SDK

[![pypi](https://img.shields.io/pypi/v/journyio-sdk?color=%234d84f5&style=flat-square)](https://pypi.org/project/journyio-sdk) ![pypi downloads](https://img.shields.io/pypi/dm/journyio-sdk?color=%234d84f5&style=flat-square) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is the official Python SDK for [journy.io](https://journy.io?utm_source=github&utm_content=readme-python-sdk).

## 💾 Installation

You can use the python package manager (`pip`) to install the SDK:

```bash
pip install journyio-sdk
```

## 🔌 Getting started

### Import

To start, first import the client.

```python
from journyio.client import Client, Config
```

### Configuration

To be able to use the journy.io SDK you need to generate an API key. If you don't have one you can create one
in [journy.io](https://system.journy.io?utm_source=github&utm_content=readme-python-sdk).

If you don't have an account yet, you can create one
in [journy.io](https://system.journy.io/register?utm_source=github&utm_content=readme-python-sdk)
or [request a demo first](https://www.journy.io/book-demo?utm_source=github&utm_content=readme-python-sdk).

Go to your settings, under the _Connections_-tab, to create and edit API keys. Make sure to give the correct permissions
to the API Key.

```python
from journyio.httpclient import HttpClientRequests

config = Config("api-key-secret")
http_client = HttpClientRequests()  # If wanted, an own implementation of the HttpClient interface can be created
client = Client(http_client, config)
```

### Methods

#### Get API key details

```python
from journyio.results import Success

result = client.get_api_key_details()
if isinstance(result, Success):
    print(result.request_id)  # str
    print(result.calls_remaining)  # int
    print(result.data)  # ApiKeyDetails
    print(result.permissions)  # list of strings denoting the permissions
```

### Handling errors

Every call will return a `Success` or `Failure` object. `Success` objects refer to the call having succeeded (and
optionally containing data). A `Failure` object refers to the API returning an error. This can be any `APIError` (too
many requests, not found...). Our SDK only throws `JournyExceptions`, no other exceptions should be
called. `JournyExceptions` are provided with useful messages, which state where the error was made.

```python
from journyio.utils import JournyException

try:
    result = client.get_tracking_snippet("www.journy.io")
    if isinstance(result, Success):
        print(result.request_id)  # str
        print(result.calls_remaining)  # int
        print(result.data)  # TrackingSnippetResonse
    else:
        print(result.request_id)  # str
        print(result.calls_remaining)  # int
        print(result.error)  # APIError
except JournyException as e:
    print(e.msg)  # str with error message
```

The request ID can be useful when viewing API logs
in [journy.io](https://system.journy.io?utm_source=github&utm_content=readme-python-sdk).

## 📬 API Docs

[API reference](https://developers.journy.io)

## 💯 Tests

To run the tests:

```bash
cd tests
pip install -r requirements.txt
pip install -U pytest
python scripts/createversion.py 0.0.0
pytest
```

## ❓ Help

We welcome your feedback, ideas and suggestions. We really want to make your life easier, so if we’re falling short or
should be doing something different, we want to hear about it.

Please create an issue or contact us via the chat on our website.

## 🔒 Security

If you discover any security related issues, please email security at journy io instead of using the issue tracker.

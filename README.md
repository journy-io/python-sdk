[![journy.io](https://raw.githubusercontent.com/journy-io/python-sdk/main/banner.png?token=AIYSKXPKLRTOT3S4HQDXE2DAGPNL4)](https://journy.io/?utm_source=github&utm_content=readme-python-sdk)

# journy.io Python SDK

[![pypi](https://img.shields.io/pypi/v/journyio-sdk?color=%234d84f5&style=flat-square)](https://pypi.org/project/journyio-sdk)

This is the official Python SDK for [journy.io](https://journy.io?utm_source=github&utm_content=readme-python-sdk).

## 💾 Installation

You can use the python package manager (`pip`) to install the SDK:

```bash
pip install journyio-sdk
```

## 🔌 Getting started

### Import

To start, first import the client.

```pyhton
from journyio.client import Client, Config
```

### Configuration

To be able to use the journy.io SDK you need to generate an API key. If you don't have one you can create one
in [journy.io](https://system.journy.io?utm_source=github&utm_content=readme-python-sdk).

If you don't have an account yet, you can create one
in [journy.io](https://system.journy.io/register?utm_source=github&utm_content=readme-python-sdk)
or [request a demo first](https://www.journy.io/book-demo?utm_source=github&utm_content=readme-python-sdk).

Go to your settings, under the *Connections*-tab, to create and edit API keys. Make sure to give the correct permissions
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

#### Create or update user

_Note: when sending an empty value (`""`) as value for a property, the property will be deleted._

```python
from journyio.client import Properties

properties = Properties()
properties["property1"] = "value1"
result = client.upsert_user("name@domain.tld", "userId", properties)
if isinstance(result, Success):
    print(result.request_id)  # str
    print(result.calls_remaining)  # int
    print(result.data)  # None
```

#### Create or update account

_Note: when sending an empty value (`""`) as value for a property, the property will be deleted._

```python
properties = Properties()
properties["property1"] = "value1"
properties["property2"] = ""  # property2 will be deleted
result = client.upsert_account("accountId", "accountName", properties, ["memberId1", "memberId2"])
if isinstance(result, Success):
    print(result.request_id)  # str
    print(result.calls_remaining)  # int
    print(result.data)  # None
```

#### Link web visitor to an app user

You can link a web visitor to a user in your application when you have our snippet installed on your website. The
snippet sets a cookie named `__journey`. If the cookie exists, you can link the web visitor to the user that is
currently logged in:

```python
result = client.link("userId", "deviceId")
if isinstance(result, Success):
    print(result.request_id)  # str
    print(result.calls_remaining)  # int
    print(result.data)  # None
```

To get the cookies you can use:

*Flask*

```python
@app.route('/...')
def method():
    device_id = request.cookies.get('__journey')
    if device_id:
        ...
    ...
```

*Django*

```python
def method(request):
    device_id = request.COOKIES.get('__journey')
    if device_id:
        ...
    ...
```

#### Add event

```python
from datetime import datetime
from journyio.events import Event, Metadata

metadata = Metadata()
metadata["metadata1"] = "value1"
event = Event()
    .for_user_in_account("accountName", "userId", "accountId")
    .happened_at(datetime.now())
    .with_metadata(metadata)
result = client.add_event(event)
if isinstance(result, Success):
    print(result.request_id)  # str
    print(result.calls_remaining)  # int
    print(result.data)  # None
```

#### Get tracking snippet for a domain

```python
from journyio.results import Success

result = client.get_tracking_snippet("www.journy.io")
if isinstance(result, Success):
    print(result.request_id)  # str
    print(result.calls_remaining)  # int
    print(result.data)  # TrackingSnippetResonse
    print(result.domain)  # str
    print(result.snippet)  # str
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
pip3 install -r requirements.txt
pytest
```

## ❓ Help

We welcome your feedback, ideas and suggestions. We really want to make your life easier, so if we’re falling short or
should be doing something different, we want to hear about it.

Please create an issue or contact us via the chat on our website.

## 🔒 Security

If you discover any security related issues, please email hans at journy io instead of using the issue tracker.

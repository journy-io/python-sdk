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

#### Create or update user

💡 A user ID should be a robust, static, unique identifier that you recognize a user by in your own systems. Because these IDs are consistent across a customer’s lifetime, you should include a user ID in identify calls as often as you can. Ideally, the user ID should be a database ID.

💡 journy.io does not recommend using simple email addresses or usernames as user ID, as these can change over time. journy.io recommends that you use static IDs instead, so the IDs never change. When you use a static ID, you can still recognize the user in your analytics tools, even if the user changes their email address.

💡 The properties `full_name`, `first_name`, `last_name`, `phone` and `registered_at` will be used for creating contacts in destinations like Intercom, HubSpot, Salesforce, ...

```python
from journyio.client import Properties
from journyio.user_identified import UserIdentified
from datetime import datetime

user = UserIdentified("userId", "name@domain.tld")
# or
user = UserIdentified.by_user_id("userId")
# or
user = UserIdentified.by_email("name@domain.tld")

properties = Properties()
properties["full_name"] = "John Doe"
properties["first_name"] = "John"
properties["last_name"] = "Doe"
properties["phone"] = "123"
properties["is_admin"] = True
properties["registered_at"] = datetime.now()
properties["age"] = 26
properties["array_of_values"] = ["value1", "value2"]
properties["key_with_empty_value"] = ""
properties["this_property_will_be_deleted"] = None

result = client.upsert_user(user, properties)
if isinstance(result, Success):
    print(result.request_id)  # str
    print(result.calls_remaining)  # int
    print(result.data)  # None
```

#### Delete user

```python
from journyio.client import Properties
from journyio.user_identified import UserIdentified
from datetime import datetime

user = UserIdentified("userId", "name@domain.tld")
# or
user = UserIdentified.by_user_id("userId")
# or
user = UserIdentified.by_email("name@domain.tld")

result = client.delete_user(user)
if isinstance(result, Success):
    print(result.request_id)  # str
    print(result.calls_remaining)  # int
    print(result.data)  # None
```

#### Create or update account

💡 An account ID should be a robust, static, unique identifier that you recognize an account by in your own systems. Ideally, the account ID should be a database ID.

💡 The properties `name`, `mrr`, `plan` and `registered_at` will be used to create companies in destinations like Intercom, HubSpot, Salesforce, ...

```python
from journyio.account_identified import AccountIdentified
from journyio.user_identified import UserIdentified
from datetime import datetime

account = AccountIdentified("accountId", "www.domain.tld")
# or
account = AccountIdentified.by_account_id("accountId")
# or
account = AccountIdentified.by_domain("www.domain.tld")

properties = Properties()
properties["name"] = "ACME, Inc"
properties["mrr"] = 399
properties["plan"] = "Pro"
properties["registered_at"] = datetime.now()
properties["is_paying"] = True
properties["array_of_values"] = ["value1", "value2"]
properties["key_with_empty_value"] = ""
properties["this_property_will_be_deleted"] = None

result = client.upsert_account(account, properties)
if isinstance(result, Success):
    print(result.request_id)  # str
    print(result.calls_remaining)  # int
    print(result.data)  # None
```

#### Delete account

```python
from journyio.account_identified import AccountIdentified
from journyio.user_identified import UserIdentified
from datetime import datetime

account = AccountIdentified("accountId", "www.domain.tld")
# or
account = AccountIdentified.by_account_id("accountId")
# or
account = AccountIdentified.by_domain("www.domain.tld")

result = client.delete_account(account)
if isinstance(result, Success):
    print(result.request_id)  # str
    print(result.calls_remaining)  # int
    print(result.data)  # None
```

#### Add user(s) to an account

```python
from journyio.account_identified import AccountIdentified
from journyio.user_identified import UserIdentified

account = AccountIdentified.by_account_id("accountId")

user1 = UserIdentified.by_user_id("memberId1")
user2 = UserIdentified.by_email("member2@domain.tld")

result = client.add_users_to_account(account, [user1, user2])
if isinstance(result, Success):
    print(result.request_id)  # str
    print(result.calls_remaining)  # int
    print(result.data)  # None
```

#### Remove user(s) from an account

When removing a user, the user will still be stored in journy.io, but marked as "removed".

```python
from journyio.account_identified import AccountIdentified
from journyio.user_identified import UserIdentified

account = AccountIdentified.by_domain("www.domain.tld")

user1 = UserIdentified.by_user_id("memberId1")
user2 = UserIdentified.by_email("member2@domain.tld")

result = client.remove_users_from_account(account, [user1, user2])
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
from journyio.user_identified import UserIdentified

user = UserIdentified("userId", "name@domain.tld")
# or
user = UserIdentified.by_user_id("userId")
# or
user = UserIdentified.by_email("name@domain.tld")

result = client.link(user, "deviceId")
if isinstance(result, Success):
    print(result.request_id)  # str
    print(result.calls_remaining)  # int
    print(result.data)  # None
```

To get the cookies (for the `deviceId`) you can use:

_Flask_

```python
@app.route('/...')
def method():
    device_id = request.cookies.get('__journey')
    if device_id:
        ...
    ...
```

_Django_

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
from journyio.account_identified import AccountIdentified
from journyio.user_identified import UserIdentified

account = AccountIdentified("accountId", "www.domain.tld")
user = UserIdentified("userId", "name@domain.tld")

metadata = Metadata()
metadata["metadata1"] = "value1"
event = Event()
    .for_user_in_account("settings_updated", user, account)
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

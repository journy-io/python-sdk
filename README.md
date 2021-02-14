[![journy.io](banner.png)](https://journy.io/?utm_source=github&utm_content=readme-python-sdk)

# journy.io Python SDK

This is the official Python SDK for [journy.io](https://journy.io?utm_source=github&utm_content=readme-python-sdk).

## 💾 Installation

You can use the python package manager (`pip`) to install the SDK:

```bash
pip install journyio-python-sdk
```

## 🔌 Getting started

### Import

To start, first import the client.

```pyhton

```

### Configuration

To be able to use the journy.io SDK you need to generate an API key. If you don't have one you can create one in [journy.io](https://system.journy.io?utm_source=github&utm_content=readme-python-sdk).

If you don't have an account yet, you can create one in [journy.io](https://system.journy.io/register?utm_source=github&utm_content=readme-python-sdk) or [request a demo first](https://www.journy.io/book-demo?utm_source=github&utm_content=readme-python-sdk).

Go to your settings, under the *Connections*-tab, to create and edit API keys. Make sure to give the correct permissions to the API Key.

```python

```

### Methods

#### Get API key details

```python

```

#### Create or update user

_Note: when sending an empty value (`""`) as value for a property, the property will be deleted._

```python

```

#### Create or update account

_Note: when sending an empty value (`""`) as value for a property, the property will be deleted._

```python

```

#### Link web visitor to an app user

You can link a web visitor to a user in your application when you have our snippet installed on your website. The snippet sets a cookie named `__journey`. If the cookie exists, you can link the web visitor to the user that is currently logged in:

```python

```

#### Add event

```python

```

#### Get tracking snippet for a domain

```python

```

### Handling errors

Every call will return a result, we don't throw errors when a call fails. We don't want to break your application when things go wrong. An exception will be thrown for required arguments that are empty or missing.


```python

```

The request ID can be useful when viewing API logs in [journy.io](https://system.journy.io?utm_source=github&utm_content=readme-python-sdk).


## 📬 API Docs

[API reference](https://developers.journy.io)

## 💯 Tests

To run the tests:

```bash
pytest
```

## ❓ Help

We welcome your feedback, ideas and suggestions. We really want to make your life easier, so if we’re falling short or should be doing something different, we want to hear about it.

Please create an issue or contact us via the chat on our website.

## 🔒 Security

If you discover any security related issues, please email hans at journy io instead of using the issue tracker.

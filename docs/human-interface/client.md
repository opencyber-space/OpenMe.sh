
## Session Client Library Documentation

### 1. Introduction

The `session_client_lib` library provides a convenient interface for interacting with the session management system, facilitating session creation, message sending, asynchronous response handling via NATS, and session rejection. It abstracts the underlying REST API calls and NATS messaging, offering a high-level API for seamless integration into client applications.

### 2. Installation

Install the library using pip:

```bash
pip install session_client_lib
```


### 3. Dependencies

The library requires the following dependencies:

- `requests`: For making HTTP requests to the session management API.
- `nats-py`: For asynchronous communication with the NATS messaging system.
- `asyncio`: For asynchronous operations (may be required explicitly for Python versions < 3.7).

These dependencies are automatically installed when you install the library via pip.

### 4. Usage

#### 4.1. Initialization

Import the `SessionClient` class from the `session_client` module and initialize it with the base URL of the session management API:

```python
from session_client import SessionClient

client = SessionClient(api_base_url="http://localhost:8000")
```

The `nats_servers` parameter is optional, defaulting to the value of the `ORG_NATS_URL` environment variable or `nats://127.0.0.1:4222` if the environment variable is not set.

#### 4.2. Creating a Session

Create a new session using the `create_session` method. This method accepts the following parameters:

- `session_id` (str, required): A unique identifier for the session.
- `message_data` (Dict[str, Any], optional): Initial message data for the session. Defaults to an empty dictionary.
- `message_data_template` (Dict[str, Any], optional): A validation template for the session's message data. Defaults to a permissive template that accepts any payload.
- `expiry_date` (int, optional): A Unix timestamp representing the session's expiration date.
- `subject_id` (str, optional): A subject identifier associated with the session.

```python
session = client.create_session(
    session_id="session123",
    message_data={"initial": "data"},
    expiry_date=1700000000,
    subject_id="subjectXYZ"
)
print("Session created:", session)
```


#### 4.3. Sending a Message and Waiting for a Response

To send a message to the human communication channel and wait for a response via NATS, use the `send_and_wait_for_response` method:

```python
try:
    response = client.send_and_wait_for_response(
        session_id="session123",
        channel_id="channelABC",
        message="Please confirm your details.",
        subject_id="subjectXYZ",
        timeout=120
    )
    print("Received response:", response)
except Exception as e:
    print("Error waiting for response:", e)
```

This method blocks until a response is received on the NATS subject or the timeout is reached.

#### 4.4. Rejecting a Session

To reject (cancel) a session, use the `reject_session` method:

```python
client.reject_session("session123")
```


#### 5. API Reference

##### `SessionClient` class

###### `__init__(self, api_base_url: str, nats_servers: Optional[list] = None)`

Initializes a new `SessionClient` instance.

- `api_base_url` (str): Base URL for REST APIs (e.g., `http://localhost:8000`).
- `nats_servers` (list, optional): List of NATS server URLs. Defaults to the value of the `ORG_NATS_URL` environment variable or `nats://127.0.0.1:4222` if the environment variable is not set.


###### `create_session(self, session_id: str, message_data: Optional[Dict[str, Any]] = None, message_data_template: Optional[Dict[str, Any]] = None, expiry_date: Optional[int] = None, subject_id: Optional[str] = None) -> Dict[str, Any]`

Creates a new session.

- `session_id` (str): Unique session identifier.
- `message_data` (Dict[str, Any], optional): Initial message data for the session. Defaults to an empty dictionary.
- `message_data_template` (Dict[str, Any], optional): A validation template for the session's message data. Defaults to a permissive template that accepts any payload.
- `expiry_date` (int, optional): A Unix timestamp representing the session's expiration date.
- `subject_id` (str, optional): A subject identifier associated with the session.

Returns: A dictionary containing the created session details.

###### `send_message(self, session_id: str, channel_id: str, message: str) -> Dict[str, Any]`

Sends a message to the human communication channel.

- `session_id` (str): The ID of the session.
- `channel_id` (str): The ID of the channel to send the message to.
- `message` (str): The content of the message to send.

Returns: A dictionary containing the response from the API.

###### `expire_sessions(self) -> Dict[str, Any]`

Triggers the expiry process to mark expired sessions.

Returns: A dictionary containing the API response.

###### `reject_session(self, session_id: str) -> Dict[str, Any]`

Rejects (cancels) a session by updating its status to 'FAILED'.

- `session_id` (str): The ID of the session to reject.

Returns: A dictionary containing the API response.

###### `send_and_wait_for_response(self, session_id: str, channel_id: str, message: str, subject_id: str, timeout: int = 60) -> Dict[str, Any]`

Sends a message and waits synchronously for the response from NATS.

- `session_id` (str): The ID of the session.
- `channel_id` (str): The ID of the channel to send the message to.
- `message` (str): The content of the message to send.
- `subject_id` (str): The subject ID to listen for the NATS response.
- `timeout` (int, optional): The timeout in seconds to wait for the response. Defaults to 60 seconds.

Returns: A dictionary containing the response message payload.

Raises: An exception if the message cannot be sent or if the timeout is reached before a response is received.



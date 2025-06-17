# Channel Communication via Webhooks

## 1. Introduction

This system enables integration with external communication platforms (like Slack, Microsoft Teams, Discord, etc.) through a **channel-based webhook mechanism**. Each channel represents a separately deployed web server that implements a platform-specific protocol.

Key principles:

* Each message sent to a channel includes a unique `session_id`.
* The external channel server receives the message and processes it (e.g., sends to Slack).
* The channel must call back a specified `response_url` with the `session_id` and result payload.
* The backend forwards this result to a `SESSIONS_SERVER`.

---

## 2. Channel Schema

### Python Dataclass

```python
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class ChannelStoreObject:
    channel_id: str = ''
    channel_name: str = ''
    channel_description: str = ''
    channel_metadata: Dict[str, Any] = field(default_factory=dict)
    channel_tags: List[str] = field(default_factory=list)
```

### Field Explanation

| Field                 | Type        | Description                                             |
| --------------------- | ----------- | ------------------------------------------------------- |
| `channel_id`          | `str`       | Unique identifier for the channel                       |
| `channel_name`        | `str`       | Human-readable name for display                         |
| `channel_description` | `str`       | Optional description of what the channel does           |
| `channel_metadata`    | `dict`      | Must include `endpoint_url` used to deliver messages    |
| `channel_tags`        | `List[str]` | Searchable labels (e.g. platform, purpose, environment) |

---

## 3. Onboarding External Channel

### Step-by-Step Walkthrough

#### Step 1: Write an External Server

The external server:

* Exposes a `POST /incoming` endpoint.
* Accepts a message with `session_id`, `message`, and `response_url`.
* Sends the `message` to the appropriate platform (e.g., Slack).
* Calls back to `response_url` with `session_id` and `response_data`.

### Example Flask Server

```python
from flask import Flask, request, jsonify
import requests
import logging
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/incoming', methods=['POST'])
def receive_message():
    try:
        data = request.json
        session_id = data.get("session_id")
        message = data.get("message")
        response_url = data.get("response_url")

        if not session_id or not message or not response_url:
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        logging.info(f"Received message for session {session_id}: {message}")

        # Simulated message send
        time.sleep(1)

        response_payload = {
            "session_id": session_id,
            "response_data": {
                "text": f"Received message: '{message}'",
                "platform": "Slack (simulated)",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }

        requests.post(response_url, json=response_payload, timeout=5)

        return jsonify({"success": True, "message": "Response sent"}), 200

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
```

#### Step 2: Register the Channel

Create the document in MongoDB:

```json
{
  "channel_id": "slack-sim",
  "channel_name": "Slack Simulated Channel",
  "channel_description": "Sends messages to Slack (simulated)",
  "channel_tags": ["slack", "test"],
  "channel_metadata": {
    "endpoint_url": "http://localhost:5001/incoming"
  }
}
```

---

## 4. Channel Management APIs

### Create Channel

```
POST /channel
```

**Body:**

```json
{
  "channel_id": "slack-sim",
  "channel_name": "Slack Simulated Channel",
  "channel_description": "Sends to Slack",
  "channel_tags": ["slack", "test"],
  "channel_metadata": {
    "endpoint_url": "http://localhost:5001/incoming"
  }
}
```

**Curl:**

```bash
curl -X POST http://localhost:8000/channel \
  -H "Content-Type: application/json" \
  -d '{
    "channel_id": "slack-sim",
    "channel_name": "Slack Simulated Channel",
    "channel_description": "Sends to Slack",
    "channel_tags": ["slack"],
    "channel_metadata": {"endpoint_url": "http://localhost:5001/incoming"}
  }'
```

---

### Get Channel

```
GET /channel/<channel_id>
```

```bash
curl http://localhost:8000/channel/slack-sim
```

---

### Update Channel

```
PUT /channel/<channel_id>
```

```bash
curl -X PUT http://localhost:8000/channel/slack-sim \
  -H "Content-Type: application/json" \
  -d '{"channel_description": "Updated"}'
```

---

### Delete Channel

```
DELETE /channel/<channel_id>
```

```bash
curl -X DELETE http://localhost:8000/channel/slack-sim
```

---

### Query Channels

```
POST /channels
```

**Example:**

```bash
curl -X POST http://localhost:8000/channels \
  -H "Content-Type: application/json" \
  -d '{"channel_tags": {"$in": ["slack"]}}'
```

---

## 5. Message Sending API

Used to send a message to an external channel based on `channel_id`.

### Endpoint

```
POST /channel/message
```

### Body

```json
{
  "channel_id": "slack-sim",
  "session_id": "abc123",
  "message": "Hello, Slack!",
  "response_url": "http://localhost:8000/webhook-response"
}
```

### Curl

```bash
curl -X POST http://localhost:8000/channel/message \
  -H "Content-Type: application/json" \
  -d '{
    "channel_id": "slack-sim",
    "session_id": "abc123",
    "message": "Hello, Slack!",
    "response_url": "http://localhost:8000/webhook-response"
  }'
```

---

## 6. Webhook Callback API

This is the endpoint that external channels must call once they complete processing.

### Endpoint

```
POST /webhook-response
```

### Body

```json
{
  "session_id": "abc123",
  "response_data": {
    "text": "Message received and handled",
    "platform": "Slack",
    "timestamp": "2025-05-27T21:10:00Z"
  }
}
```

---



# Session Messages API Documentation

## 1. Introduction

The **Session Messages API** enables the creation, retrieval, updating, deletion, and querying of session-level messages in a communication or workflow system. Each message is tied to a unique session and can be delivered via external channels like Slack, Teams, etc. This API interacts with a MongoDB-backed data store and is designed to support asynchronous message dispatch and tracking.

---

## 2. Session Schema

### Dataclass

```python
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class SessionMessage:
    session_id: str = ''
    subject_id: str = ''
    message_data: Dict[str, Any] = field(default_factory=dict)
    message_data_template: Dict[str, Any] = field(default_factory=dict)
    reception_channel_id: str = ''
    expiry_date: int = 0
    status: str = 'pending'
    dsl_execution_id: str = ''
```

### Field Explanation

| Field                   | Type             | Description                                                                 |
| ----------------------- | ---------------- | --------------------------------------------------------------------------- |
| `session_id`            | `str`            | Unique identifier for the session                                           |
| `subject_id`            | `str`            | Identifier for the user or entity associated with the message               |
| `message_data`          | `Dict[str, Any]` | Actual message content in key-value structure                               |
| `message_data_template` | `Dict[str, Any]` | Optional templated message form, useful for rendering                       |
| `reception_channel_id`  | `str`            | ID of the channel used to send the message (e.g., Slack, Teams)             |
| `expiry_date`           | `int`            | Epoch timestamp indicating when the message expires                         |
| `status`                | `str`            | Status of the message, e.g., `pending`, `sent`, `expired`                   |
| `dsl_execution_id`      | `str`            | Identifier of the DSL execution that generated this message (if applicable) |

---

## 3. API Endpoints

### 3.1 Create Session Message

**Endpoint:**

```
POST /session
```

**Description:**
Creates a new session message entry.

**Curl Example:**

```bash
curl -X POST http://localhost:8000/session \
     -H "Content-Type: application/json" \
     -d '{
           "session_id": "abc123",
           "subject_id": "user789",
           "message_data": {"text": "Hello, user!"},
           "message_data_template": {},
           "reception_channel_id": "slack-sim",
           "expiry_date": 1700000000,
           "status": "pending",
           "dsl_execution_id": "exec-456"
         }'
```

---

### 3.2 Get Session Message by ID

**Endpoint:**

```
GET /session/<session_id>
```

**Curl Example:**

```bash
curl http://localhost:8000/session/abc123
```

---

### 3.3 Update Session Message

**Endpoint:**

```
PUT /session/<session_id>
```

**Curl Example:**

```bash
curl -X PUT http://localhost:8000/session/abc123 \
     -H "Content-Type: application/json" \
     -d '{"status": "sent"}'
```

---

### 3.4 Delete Session Message

**Endpoint:**

```
DELETE /session/<session_id>
```

**Curl Example:**

```bash
curl -X DELETE http://localhost:8000/session/abc123
```

---

### 3.5 Query Session Messages

**Endpoint:**

```
POST /sessions
```

**Description:**
Allows filtering session messages using Mongo-style filters.

**Curl Example:**

```bash
curl -X POST http://localhost:8000/sessions \
     -H "Content-Type: application/json" \
     -d '{"status": "pending", "reception_channel_id": "slack-sim"}'
```

---

from typing import Optional
from datetime import datetime, timezone
import time
import logging
import re
import json
from typing import Dict, Any, Tuple, Union, List
from nats.aio.client import Client as NATS
import asyncio

from .db import SessionMessage, SessionMessageDatabase
from .schema import ValidationResult, SessionStatus
from .channels import ChannelsClient

logger = logging.getLogger(__name__)


class NatsPublisher:
    def __init__(self, servers: list):

        self.servers = servers
        self.nc = NATS()
        self.loop = asyncio.get_event_loop()

    async def connect(self):
        await self.nc.connect(servers=self.servers, loop=self.loop)
        logger.info("Connected to NATS servers: %s", self.servers)

    async def publish_human_intervention_result(self, subject_id: str, message_response: dict):
        topic = f"{subject_id}__human_intervention_results"
        payload = {
            "event_type": "human_intervention_results",
            "sender_subject_id": "sessions_system",
            "event_payload": message_response
        }
        data = json.dumps(payload).encode()
        await self.nc.publish(topic, data)
        logger.info("Published human intervention result to topic %s", topic)

    async def close(self):
        await self.nc.drain()
        await self.nc.close()
        logger.info("NATS connection closed")


class DynamicValidator:

    def __init__(self, template: Dict[str, Any]):
        self.template = template
        self.input_schema = template.get("policy_input_schema", {})

    def validate(self, message_data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        errors = {}

        for field, rules in self.input_schema.items():
            # Check presence
            if field not in message_data:
                errors[field] = "Missing required field"
                continue

            value = message_data[field]
            expected_type = rules.get("type")

            # Validate type
            if expected_type and not self._check_type(value, expected_type):
                errors[field] = f"Expected type '{expected_type}', got '{type(value).__name__}'"
                continue

            # Validate based on type
            if expected_type == "string":
                self._validate_string(field, value, rules, errors)
            elif expected_type == "number":
                self._validate_number(field, value, rules, errors)
            elif expected_type == "boolean":
                # No extra validation needed for boolean
                pass
            elif expected_type == "array":
                self._validate_array(field, value, rules, errors)
            elif expected_type == "object":
                # Nested object validation could be added here if schema provided
                pass
            elif expected_type == "any":
                # Accept anything
                pass
            else:
                # Unknown type
                errors[field] = f"Unsupported type '{expected_type}' in schema"

            # Validate enum
            if "enum" in rules:
                if value not in rules["enum"]:
                    errors[field] = f"Value '{value}' not in allowed set {rules['enum']}"

        is_valid = len(errors) == 0
        return is_valid, errors

    def _check_type(self, value: Any, expected_type: str) -> bool:
        type_map = {
            "string": str,
            "boolean": bool,
            "number": (int, float),
            "array": list,
            "object": dict,
            "any": object,
        }
        python_type = type_map.get(expected_type)
        if python_type is None:
            return False
        if expected_type == "any":
            return True
        return isinstance(value, python_type)

    def _validate_string(self, field: str, value: str, rules: Dict[str, Any], errors: Dict[str, str]) -> None:
        # pattern
        pattern = rules.get("pattern")
        if pattern and not re.match(pattern, value):
            errors[field] = f"Value '{value}' does not match pattern '{pattern}'"
            return

        # minLength
        min_length = rules.get("minLength")
        if min_length is not None and len(value) < min_length:
            errors[field] = f"Length {len(value)} is less than minimum length {min_length}"
            return

        # maxLength
        max_length = rules.get("maxLength")
        if max_length is not None and len(value) > max_length:
            errors[field] = f"Length {len(value)} exceeds maximum length {max_length}"
            return

    def _validate_number(self, field: str, value: Union[int, float], rules: Dict[str, Any], errors: Dict[str, str]) -> None:
        # minimum
        minimum = rules.get("minimum")
        if minimum is not None and value < minimum:
            errors[field] = f"Value {value} is less than minimum {minimum}"
            return

        # maximum
        maximum = rules.get("maximum")
        if maximum is not None and value > maximum:
            errors[field] = f"Value {value} exceeds maximum {maximum}"
            return

        # exclusiveMinimum
        exclusive_min = rules.get("exclusiveMinimum")
        if exclusive_min is not None and value <= exclusive_min:
            errors[field] = f"Value {value} must be greater than exclusive minimum {exclusive_min}"
            return

        # exclusiveMaximum
        exclusive_max = rules.get("exclusiveMaximum")
        if exclusive_max is not None and value >= exclusive_max:
            errors[field] = f"Value {value} must be less than exclusive maximum {exclusive_max}"
            return

    def _validate_array(self, field: str, value: List[Any], rules: Dict[str, Any], errors: Dict[str, str]) -> None:
        # minItems
        min_items = rules.get("minItems")
        if min_items is not None and len(value) < min_items:
            errors[field] = f"Array length {len(value)} is less than minimum items {min_items}"
            return

        max_items = rules.get("maxItems")
        if max_items is not None and len(value) > max_items:
            errors[field] = f"Array length {len(value)} exceeds maximum items {max_items}"
            return

        unique_items = rules.get("uniqueItems")
        if unique_items:
            if len(set(value)) != len(value):
                errors[field] = "Array items are not unique"
                return
        items_schema = rules.get("items")
        if items_schema:
            for i, item in enumerate(value):
                if not self._check_type(item, items_schema.get("type", "any")):
                    errors[field] = f"Item at index {i} expected type '{items_schema.get('type')}', got '{type(item).__name__}'"
                    return
                # For string items, validate pattern if any
                if items_schema.get("type") == "string" and "pattern" in items_schema:
                    pattern = items_schema["pattern"]
                    if not re.match(pattern, item):
                        errors[field] = f"Item at index {i} with value '{item}' does not match pattern '{pattern}'"
                        return


class SessionManagementService:
    def __init__(self, db: SessionMessageDatabase, channels_client: ChannelsClient, nats_publisher: NatsPublisher):
        self.db = db
        self.channels_client = channels_client

    def create_session(self, session_message: SessionMessage) -> SessionMessage:
        success, result = self.db.insert(session_message)
        if not success:
            raise Exception(f"Failed to create session: {result}")
        return session_message

    def process_incoming_message(self, session_id: str, message_data: dict) -> ValidationResult:
        success, session_or_error = self.db.get_by_session_id(session_id)
        if not success:
            return ValidationResult(is_valid=False, errors={"error": session_or_error})

        session = session_or_error
        # Update message_data
        session.message_data.update(message_data)

        new_status = "pending"
        self.db.update(
            session_id, {"message_data": session.message_data, "status": new_status})

        return True

    def validate_message(self, session_message: SessionMessage) -> ValidationResult:
        validator = DynamicValidator(session_message.message_data_template)
        is_valid, errors = validator.validate(session_message.message_data)
        return ValidationResult(is_valid=is_valid, errors=errors, validated_at=int(time.time()))

    def update_session_status(self, session_id: str, status: SessionStatus) -> bool:
        success, _ = self.db.update(session_id, {"status": status.value})
        return success

    def expire_sessions(self) -> None:
        current_ts = int(time.time())
        filter_expired = {
            "expiry_date": {"$lt": current_ts},
            "status": {"$ne": SessionStatus.EXPIRED.value}
        }
        success, sessions = self.db.query(filter_expired)
        if not success:
            # Log or handle error
            return

        for session_doc in sessions:
            session_id = session_doc.get("session_id")
            if session_id:
                self.update_session_status(session_id, SessionStatus.EXPIRED)

    def send_message_to_channel(self, session_id: str, channel_id: str, message: str) -> Tuple[bool, Any]:
        success, result = self.channels_client.send_message(
            channel_id, session_id, message)
        if success:
            logger.info(
                f"Message sent to channel {channel_id} for session {session_id}")
        else:
            logger.warning(
                f"Failed to send message to channel {channel_id} for session {session_id}: {result}")
        return success, result

    def process_channel_response(self, session_id: str, response_data: Dict[str, Any]) -> Tuple[bool, Any]:

        success, session_or_error = self.db.get_by_session_id(session_id)
        if not success:
            logger.error(f"Session {session_id} not found: {session_or_error}")
            return False, {"error": f"Session not found: {session_or_error}"}

        session: SessionMessage = session_or_error

        session.message_data.update(response_data)

        validation_result: ValidationResult = self.validate_message(session)

        new_status = SessionStatus.VALIDATED.value if validation_result.is_valid else SessionStatus.FAILED.value

        # Update session in DB with new message_data and status
        update_success, update_result = self.db.update(
            session_id,
            {
                "message_data": session.message_data,
                "status": new_status,
                "last_validated_at": validation_result.validated_at
            }
        )

        if not update_success:
            logger.error(
                f"Failed to update session {session_id}: {update_result}")
            return False, {"error": f"Failed to update session: {update_result}"}

        logger.info(f"Session {session_id} updated with status {new_status}")

        if update_success:
            # Assuming session has subject_id field
            subject_id = session_or_error.subject_id
            try:
                asyncio.run(self.nats_publisher.publish_human_intervention_result(
                    subject_id, response_data))
            except Exception as e:
                logger.error(
                    f"Failed to publish human intervention result for session {session_id}: {e}")

        return update_success, {
            "status": new_status,
            "validation_errors": validation_result.errors
        }

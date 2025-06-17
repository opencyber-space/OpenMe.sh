import os
import requests
import json
import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)


class ChannelsClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.response_url = os.getenv(
            "SESSIONS_SERVER_URL", "http://localhost:8000") + "/webhook-response"

    def send_message(
        self,
        channel_id: str,
        session_id: str,
        message: str
    ) -> Tuple[bool, Dict[str, Any]]:
        url = f"{self.base_url}/channel/message"
        payload = {
            "channel_id": channel_id,
            "session_id": session_id,
            "message": message,
            "response_url": self.response_url
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                logger.info(
                    f"Message sent to channel '{channel_id}' successfully.")
                return True, response.json()
            else:
                logger.warning(
                    f"Failed to send message: {response.status_code} - {response.text}")
                return False, response.json()
        except Exception as e:
            logger.error(
                f"Error in sending message to channel '{channel_id}': {e}")
            return False, {"error": str(e)}


class FanoutClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    def push_message(self, topic: str, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        url = f"{self.base_url}/MESSAGES"
        message_payload = {
            "topic": topic,
            "data": data
        }

        payload = {
            "message": json.dumps(message_payload)
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                logger.info(f"Message pushed to topic '{topic}' successfully.")
                return True, response.json()
            else:
                logger.warning(
                    f"Failed to push message: {response.status_code} - {response.text}")
                return False, response.json()
        except Exception as e:
            logger.error(f"Error in pushing message to topic '{topic}': {e}")
            return False, {"error": str(e)}

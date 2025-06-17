import requests
import logging
import os
from typing import Dict, Any, Tuple

from .crud import ChannelStoreDatabase

logger = logging.getLogger(__name__)


class ChannelsClient:
  
    def send_message(self, endpoint_url: str, payload: Dict[str, Any]) -> Tuple[bool, Any]:
        
        try:
            response = requests.post(endpoint_url, json=payload, timeout=5)
            if response.status_code in [200, 202]:
                logger.info(f"Message sent successfully to {endpoint_url}")
                return True, response.json() if response.content else {}
            else:
                logger.warning(f"Channel responded with status {response.status_code}: {response.text}")
                return False, response.text
        except Exception as e:
            logger.error(f"Failed to send message to channel: {e}")
            return False, str(e)



class ChannelMessenger:
    def __init__(self):
        self.client = ChannelsClient()
        self.db = ChannelStoreDatabase()

    def send_message_to_channel(self, channel_id: str, session_id: str, message: str, response_url: str) -> Tuple[bool, Any]:
        
        try:
            success, channel_obj = self.db.get_by_channel_id(channel_id)
            if not success:
                logger.error(f"Channel {channel_id} not found: {channel_obj}")
                return False, f"Channel {channel_id} not found"

            endpoint_url = channel_obj.channel_metadata.get("endpoint_url")
            if not endpoint_url:
                logger.error(f"Missing endpoint_url in metadata for channel {channel_id}")
                return False, "Channel metadata missing 'endpoint_url'"

            payload = {
                "channel_id": channel_id,
                "session_id": session_id,
                "message": message,
                "response_url": response_url
            }

            return self.client.send_message(endpoint_url, payload)

        except Exception as e:
            logger.error(f"Error sending message to channel {channel_id}: {e}")
            return False, str(e)


class ResponseProcessor:
    def __init__(self):
        self.sessions_server_url = os.getenv("SESSIONS_SERVER")
        if not self.sessions_server_url:
            raise ValueError("SESSIONS_SERVER environment variable not set")

    def process(self, session_id: str, response_data: Dict[str, Any]) -> Tuple[bool, Any]:
       
        try:
            target_url = f"{self.sessions_server_url.rstrip('/')}/channels/response"
            payload = {
                "session_id": session_id,
                "response_data": response_data
            }

            response = requests.post(target_url, json=payload, timeout=5)

            if response.status_code in [200, 202]:
                logger.info(f"Response for session {session_id} forwarded successfully")
                return True, response.json() if response.content else {}
            else:
                logger.warning(f"Session server responded with status {response.status_code}: {response.text}")
                return False, response.text

        except Exception as e:
            logger.error(f"Failed to forward response to session server: {e}")
            return False, str(e)
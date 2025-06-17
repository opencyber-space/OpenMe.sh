import time
import uuid
import logging
from typing import Dict, Any
from .proxy import ChatProxyRouter
from .schema import ChatMessage
from .sessions import ChatMessagesDatabase

logger = logging.getLogger(__name__)


class ChatManager:
    def __init__(self, chat_proxy_router: ChatProxyRouter, message_db: ChatMessagesDatabase):
        self.proxy = chat_proxy_router
        self.db = message_db

    async def handle_message(self, session_id: str, subject_id: str, message_json: Dict[str, Any], file_urls: Dict[str, str] = None) -> Dict[str, Any]:
        file_urls = file_urls or {}

        # Step 1: Save user message
        user_msg = ChatMessage(
            chat_id=str(uuid.uuid4()),
            session_id=session_id,
            message_json=message_json,
            file_urls=file_urls,
            type="user",
            timestamp=int(time.time())
        )

        success, result = self.db.insert(user_msg)
        if not success:
            logger.warning(f"Failed to log user message: {result}")

        # Step 2: Forward to subject via proxy
        try:
            response_json = await self.proxy.forward_message(subject_id, message_json)
        except Exception as e:
            logger.error(
                f"Error forwarding message to subject {subject_id}: {e}")
            raise

        # Step 3: Save system message
        system_msg = ChatMessage(
            chat_id=str(uuid.uuid4()),
            session_id=session_id,
            message_json=response_json,
            file_urls={},
            type="system",
            timestamp=int(time.time())
        )

        success, result = self.db.insert(system_msg)
        if not success:
            logger.warning(f"Failed to log system message: {result}")

        # Step 4: Return response
        return response_json

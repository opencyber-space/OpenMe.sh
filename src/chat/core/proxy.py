import asyncio
import websockets
import json
import logging
from typing import Dict

import requests

logger = logging.getLogger(__name__)


class ChatWebSocketClient:
    def __init__(self, chat_url: str):
        self.chat_url = chat_url
        self.websocket = None
        self.lock = asyncio.Lock()

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.chat_url)
            logger.info(f"Connected to chat WebSocket at {self.chat_url}")
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            raise

    async def push(self, message: dict) -> dict:
        async with self.lock:
            if self.websocket is None or self.websocket.closed:
                await self.connect()

            try:
                await self.websocket.send(json.dumps(message))
                response = await self.websocket.recv()
                return json.loads(response)
            except Exception as e:
                logger.error(f"WebSocket error during push: {e}")
                raise


class ChatProxyRouter:
    def __init__(self, subjects_registry_url: str):
        self.subjects_registry_url = subjects_registry_url.rstrip("/")
        self.clients: Dict[str, ChatWebSocketClient] = {}
        self.lock = asyncio.Lock()

    async def get_client_for_subject(self, subject_id: str) -> ChatWebSocketClient:
        async with self.lock:
            if subject_id in self.clients:
                return self.clients[subject_id]

            try:
                resp = requests.get(
                    f"{self.subjects_registry_url}/subjects/get_subject_id",
                    params={"subject_id": subject_id}
                )
                data = resp.json()
                chat_url = data['data']['urlMap']['chatURL']
                client = ChatWebSocketClient(chat_url)
                await client.connect()
                self.clients[subject_id] = client
                return client
            except Exception as e:
                logger.error(f"Failed to get chatURL for subject {subject_id}: {e}")
                raise

    async def forward_message(self, subject_id: str, message: Dict) -> Dict:
        client = await self.get_client_for_subject(subject_id)
        return await client.push(message)
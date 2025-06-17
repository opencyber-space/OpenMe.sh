import asyncio
import websockets
import json
import logging
from .sessions import ChatMessagesDatabase
from .schema import ChatMessage

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# WebSocket clients
clients = set()
db = ChatMessagesDatabase()


async def handle_message(websocket, message):
    try:
        action = message.get("action")
        data = message.get("data", {})

        if action == "get_by_chat_id":
            chat_id = data.get("chat_id")
            success, result = db.get_by_chat_id(chat_id)
            return {"success": success, "data": result.to_dict() if success else result}

        elif action == "query_by_session":
            session_id = data.get("session_id")
            success, result = db.query_by_session(session_id)
            return {"success": success, "data": result}

        elif action == "insert":
            msg_obj = ChatMessage.from_dict(data)
            success, result = db.insert(msg_obj)
            return {"success": success, "data": {"chat_id": msg_obj.chat_id} if success else result}

        else:
            return {"success": False, "error": f"Unsupported action: {action}"}

    except Exception as e:
        logger.exception("Failed to process message")
        return {"success": False, "error": str(e)}


async def handler(websocket, path):
    clients.add(websocket)
    try:
        async for raw_msg in websocket:
            try:
                message = json.loads(raw_msg)
                response = await handle_message(websocket, message)
            except json.JSONDecodeError:
                response = {"success": False, "error": "Invalid JSON format"}

            await websocket.send(json.dumps(response))

    except websockets.exceptions.ConnectionClosed:
        logger.info("Client disconnected")
    finally:
        clients.remove(websocket)


def run_ws_server(host='0.0.0.0', port=8765):
    logger.info(f"Starting WebSocket server on ws://{host}:{port}")
    asyncio.get_event_loop().run_until_complete(websockets.serve(handler, host, port))
    asyncio.get_event_loop().run_forever()



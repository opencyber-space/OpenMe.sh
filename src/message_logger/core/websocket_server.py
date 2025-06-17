import asyncio
import websockets
import threading
import json
import redis
from config import Config

clients = set()

async def broadcast_message(message):
    if clients:  # Only broadcast if there are clients connected
        await asyncio.wait([client.send(message) for client in clients])

async def handler(websocket, path):
    clients.add(websocket)
    try:
        async for _ in websocket:
            pass
    finally:
        clients.remove(websocket)

def listen_to_redis():
    redis_conn = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)
    pubsub = redis_conn.pubsub()
    pubsub.subscribe(Config.REDIS_QUEUE)

    for message in pubsub.listen():
        if message['type'] == 'message':
            asyncio.run(broadcast_message(message['data']))

def start_websocket_server():
    start_server = websockets.serve(handler, 'localhost', 6789)
    redis_thread = threading.Thread(target=listen_to_redis)
    redis_thread.start()
    
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

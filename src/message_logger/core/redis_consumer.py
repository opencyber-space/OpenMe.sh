import redis
import threading
import time
import json
from .db import TimescaleDB
from .config import Config

class RedisConsumer:
    def __init__(self):
        self.db = TimescaleDB()
        self.redis_conn = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)
        self.messages = []

    def process_message(self, message):
        # Process the message into a tuple
        data = json.loads(message)
        return (
            data['message_uuid'],
            data['origin_ts'],
            data['ack_ts'],
            json.dumps(data['message_data']),
            data['source_subject_id'],
            data['destination_subject_ids'],
            data['topic'],
            data['message_type'],
            json.dumps(data['message_metadata'])
        )

    def batch_write(self):
        while True:
            if len(self.messages) >= Config.BATCH_SIZE or (self.messages and time.time() - self.last_write_time >= Config.BATCH_INTERVAL):
                self.db.batch_insert(self.messages)
                self.messages = []
                self.last_write_time = time.time()

    def listen_to_redis(self):
        self.last_write_time = time.time()
        while True:
            message = self.redis_conn.brpop(Config.REDIS_QUEUE)
            if message:
                self.messages.append(self.process_message(message[1]))

            self.batch_write()

def start_redis_consumer():
    consumer = RedisConsumer()
    consumer_thread = threading.Thread(target=consumer.listen_to_redis)
    consumer_thread.start()

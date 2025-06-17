import os
import redis
import logging
import traceback
import json

from .controller import MessageController


class RedisMessageReceiver:
    def __init__(self, message_controller):
        self.redis_host = os.getenv("BUFFER_RECEIVER_REDIS_HOST")
        self.redis_port = os.getenv("BUFFER_RECEIVER_REDIS_PORT")
        self.queue_name = "MESSAGES"
        self.connection = None
        self.message_controller = message_controller
        self.setup_redis_connection()

    def setup_redis_connection(self):
        try:
            self.connection = redis.Redis(host=self.redis_host, port=self.redis_port, decode_responses=True)
            logging.info("Redis connection established.")
        except Exception as e:
            logging.error(f"Error establishing Redis connection: {e}")
            logging.debug(traceback.format_exc())

    def listen(self):
        try:
            logging.info(f"Listening to queue: {self.queue_name}")
            while True:
                message = self.connection.brpop(self.queue_name)
                if message:
                    message_dict = json.loads(message[1])
                    self.message_controller.submit_message(message_dict)
        except Exception as e:
            logging.error(f"Error while listening to Redis queue: {e}")
            logging.debug(traceback.format_exc())

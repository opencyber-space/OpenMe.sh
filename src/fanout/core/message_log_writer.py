import os
import json
import redis
import logging
import traceback
from queue import Queue
from threading import Thread

class MessageLogWriter(Thread):
    def __init__(self, message_log_writer_queue):
        super().__init__()
        self.message_log_writer_queue = message_log_writer_queue
        self.redis_host = os.getenv("MESSAGE_LOG_WRITER_HOST")
        self.redis_port = os.getenv("MESSAGE_LOG_WRITER_PORT")
        self.connection = None
        self.setup_redis_connection()
        self.daemon = True

    def setup_redis_connection(self):
        try:
            self.connection = redis.Redis(host=self.redis_host, port=self.redis_port, decode_responses=True)
            logging.info("Redis connection established.")
        except Exception as e:
            logging.error(f"Error establishing Redis connection: {e}")
            logging.debug(traceback.format_exc())

    def run(self):
        try:
            while True:
                message = self.message_log_writer_queue.get()
                if message is not None:
                    message_json = json.dumps(message)
                    self.connection.rpush("MESSAGES", message_json)
                    logging.info(f"Message written to Redis queue: {message_json}")
                self.message_log_writer_queue.task_done()
        except Exception as e:
            logging.error(f"Error in MessageLogWriter: {e}")
            logging.debug(traceback.format_exc())

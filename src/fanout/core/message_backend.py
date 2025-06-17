import os
import json
import nats
import logging
import traceback
from queue import Queue
from threading import Thread


class MessageBackendWriter(Thread):
    def __init__(self, message_backend_queue):
        super().__init__()
        self.message_backend_queue = message_backend_queue
        self.nats_host = os.getenv("MESSAGE_BACKEND_NATS_HOST")
        self.nats_port = os.getenv("MESSAGE_BACKEND_NATS_PORT")
        self.connection = None
        self.setup_nats_connection()
        self.daemon = True

    def setup_nats_connection(self):
        try:
            self.connection = nats.connect(
                f"nats://{self.nats_host}:{self.nats_port}")
            logging.info("NATS connection established.")
        except Exception as e:
            logging.error(f"Error establishing NATS connection: {e}")
            logging.debug(traceback.format_exc())

    def run(self):
        try:
            while True:
                message = self.message_backend_queue.get()
                if message is not None:
                    topic = message.get("topic")
                    if topic:
                        message_json = json.dumps(message)
                        self.connection.publish(topic, message_json.encode())
                        logging.info(
                            f"Message published to NATS topic '{topic}': {message_json}")
                    else:
                        logging.warning("No 'topic' found in message")
                self.message_backend_queue.task_done()
        except Exception as e:
            logging.error(f"Error in MessageBackendWriter: {e}")
            logging.debug(traceback.format_exc())

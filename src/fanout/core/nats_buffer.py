import os
import nats
import logging
import traceback
import json

from .controller import MessageController



class NATSMessageReceiver:
    def __init__(self, message_controller):
        self.nats_host = os.getenv("BUFFER_RECEIVER_NATS_HOST")
        self.nats_port = os.getenv("BUFFER_RECEIVER_NATS_PORT")
        self.queue_name = "MESSAGES"
        self.connection = None
        self.message_controller = message_controller
        self.setup_nats_connection()

    def setup_nats_connection(self):
        try:
            self.connection = nats.connect(
                f"nats://{self.nats_host}:{self.nats_port}")
            logging.info("NATS connection established.")
        except Exception as e:
            logging.error(f"Error establishing NATS connection: {e}")
            logging.debug(traceback.format_exc())

    def listen(self):
        try:
            logging.info(f"Listening to queue: {self.queue_name}")
            while True:
                msg = self.connection.subscribe(self.queue_name)
                if msg:
                    message_dict = json.loads(msg.data.decode())
                    self.message_controller.submit_message(message_dict)
        except Exception as e:
            logging.error(f"Error while listening to NATS queue: {e}")
            logging.debug(traceback.format_exc())

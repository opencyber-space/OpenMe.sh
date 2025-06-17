import os
import logging
import traceback
from flask import Flask, request, jsonify
import json

from .controller import MessageController

class HTTPReceiver:
    def __init__(self, message_controller):
        self.queue_name = "MESSAGES"
        self.message_controller = message_controller
        self.setup_http_server()

    def setup_http_server(self):
        self.app = Flask(__name__)
        self.app.add_url_rule(f"/{self.queue_name}", view_func=self.receive_message, methods=["POST"])

    def receive_message(self):
        try:
            message = request.json.get("message")
            if message:
                message_dict = json.loads(message)
                self.message_controller.submit_message(message_dict)
                return jsonify({"status": "Message received"}), 200
            else:
                logging.warning("No message received")
                return jsonify({"error": "No message found"}), 400
        except Exception as e:
            logging.error(f"Error receiving message: {e}")
            logging.debug(traceback.format_exc())
            return jsonify({"error": "Internal server error"}), 500

    def listen(self):
        try:
            logging.info(f"HTTP server listening on /{self.queue_name}")
            self.app.run(host="0.0.0.0", port=int(os.getenv("BUFFER_RECEIVER_HTTP_PORT", 5000)))
        except Exception as e:
            logging.error(f"Error while running HTTP server: {e}")
            logging.debug(traceback.format_exc())

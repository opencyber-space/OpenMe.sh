import os
import logging
import traceback
from flask import Flask, jsonify
from flask_sock import Sock
import json

from .controller import MessageController


class WsMessageReceiver:
    def __init__(self, message_controller):
        self.queue_name = "MESSAGES"
        self.message_controller = message_controller
        self.setup_websocket_server()

    def setup_websocket_server(self):
        self.app = Flask(__name__)
        self.sock = Sock(self.app)
        self.sock.route(f"/{self.queue_name}")(self.receive_message)

    def receive_message(self, ws):
        try:
            while True:
                message = ws.receive()
                if message:
                    logging.info(f"Received message: {message}")
                    try:
                        message_dict = json.loads(message)
                        self.message_controller.submit_message(message_dict)
                        logging.info(f"Submitted message: {message_dict}")
                    except json.JSONDecodeError:
                        logging.warning("Invalid JSON format")
                        ws.send(
                            jsonify({"error": "Invalid JSON format"}).get_data(as_text=True))
                        continue

                    ws.send(
                        jsonify({"status": "Message received"}).get_data(as_text=True))
                else:
                    logging.warning("No message received")
                    ws.send(
                        jsonify({"error": "No message found"}).get_data(as_text=True))
        except Exception as e:
            logging.error(f"Error receiving WebSocket message: {e}")
            logging.debug(traceback.format_exc())
            ws.send(jsonify({"error": "Internal server error"}
                            ).get_data(as_text=True))

    def listen(self):
        try:
            logging.info(f"WebSocket server listening on /{self.queue_name}")
            self.app.run(host="0.0.0.0", port=int(
                os.getenv("BUFFER_RECEIVER_WS_PORT", 5000)))
        except Exception as e:
            logging.error(f"Error while running WebSocket server: {e}")
            logging.debug(traceback.format_exc())

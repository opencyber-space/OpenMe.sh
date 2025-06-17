import os
import logging
from queue import Queue
from threading import Thread
from . controller import MessageController
from .message_log_writer import MessageLogWriter
from .message_backend import MessageBackendWriter
from . import WsMessageReceiver


def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def run_service():
    setup_logging()

    message_log_writer_queue = Queue()
    message_backend_queue = Queue()

    message_controller = MessageController(
        message_log_writer_queue, message_backend_queue)

    message_log_writer = MessageLogWriter(message_log_writer_queue)
    message_backend_writer = MessageBackendWriter(message_backend_queue)

    ws_receiver = WsMessageReceiver(message_controller)

    log_writer_thread = Thread(target=message_log_writer.start)
    backend_writer_thread = Thread(target=message_backend_writer.start)

    log_writer_thread.start()
    backend_writer_thread.start()

    ws_receiver_thread = Thread(target=ws_receiver.listen)
    ws_receiver_thread.start()

    log_writer_thread.join()
    backend_writer_thread.join()
    ws_receiver_thread.join()

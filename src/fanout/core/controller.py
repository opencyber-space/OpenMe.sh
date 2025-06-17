import logging
import traceback


class MessageController:
    def __init__(self, message_log_writer_queue, message_backend_queue):
        self.message_log_writer_queue = message_log_writer_queue  # Infinite length queue
        self.message_backend_queue = message_backend_queue  # Infinite length queue
        logging.info("MessageController initialized with two queues.")

    def submit_message(self, message):
        try:
            self.message_log_writer_queue.put(message)
            logging.info(
                f"Message submitted to message_log_writer_queue: {message}")

            self.message_backend_queue.put(message)
            logging.info(
                f"Message submitted to message_backend_queue: {message}")
        except Exception as e:
            logging.error(f"Error submitting message to queues: {e}")
            logging.debug(traceback.format_exc())

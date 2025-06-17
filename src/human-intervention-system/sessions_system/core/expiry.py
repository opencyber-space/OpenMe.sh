import threading
import time
import logging
from typing import Optional

from .schema import SessionStatus
from .handler import SessionManagementService

logger = logging.getLogger(__name__)

class ExpiryScheduler(threading.Thread):
    def __init__(self, session_service: SessionManagementService, interval_seconds: int = 300):
       
        super().__init__()
        self.session_service = session_service
        self.interval = interval_seconds
        self._stop_event = threading.Event()
        self.daemon = True 

    def run(self):
        logger.info("ExpiryScheduler thread started, running every %d seconds", self.interval)
        while not self._stop_event.is_set():
            try:
                self._check_and_expire_sessions()
            except Exception as e:
                logger.error("Error during expiry check: %s", e)
            # Wait for the interval or until stop event is set
            self._stop_event.wait(self.interval)
        logger.info("ExpiryScheduler thread stopped")

    def _check_and_expire_sessions(self):
        
        current_ts = int(time.time())
        filter_pending_expired = {
            "status": SessionStatus.PENDING.value,
            "expiry_date": {"$lt": current_ts}
        }
        success, sessions = self.session_service.db.query(filter_pending_expired)
        if not success:
            logger.error("Failed to query pending expired sessions: %s", sessions)
            return

        logger.info("ExpiryScheduler found %d sessions to expire", len(sessions))
        for session_doc in sessions:
            session_id = session_doc.get("session_id")
            if session_id:
                updated = self.session_service.update_session_status(session_id, SessionStatus.EXPIRED)
                if updated:
                    logger.info("Session %s marked as expired", session_id)
                else:
                    logger.warning("Failed to update session %s to expired", session_id)

    def stop(self):
        
        logger.info("Stopping ExpiryScheduler thread...")
        self._stop_event.set()
        self.join()

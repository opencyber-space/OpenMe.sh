import requests
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class BackboneDBClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    def create_backbone(self, payload: Dict[str, Any]) -> Tuple[bool, Any]:
        
        try:
            response = requests.post(f"{self.base_url}/backbone", json=payload)
            if response.status_code == 201:
                return True, response.json().get("data")
            else:
                logger.warning(f"Create failed: {response.text}")
                return False, response.json()
        except requests.RequestException as e:
            logger.error(f"Request error during create_backbone: {e}")
            return False, str(e)

    def delete_backbone(self, system_id: str) -> Tuple[bool, Any]:
        
        try:
            response = requests.delete(f"{self.base_url}/backbone/{system_id}")
            if response.status_code == 200:
                return True, response.json().get("data")
            else:
                logger.warning(f"Delete failed: {response.text}")
                return False, response.json()
        except requests.RequestException as e:
            logger.error(f"Request error during delete_backbone: {e}")
            return False, str(e)

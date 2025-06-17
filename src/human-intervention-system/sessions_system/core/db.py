import os
import logging
from typing import Dict, Any, Tuple
from pymongo import MongoClient, errors
from .schema import SessionMessage 

logger = logging.getLogger(__name__)


class SessionMessageDatabase:
    def __init__(self):
        try:
            uri = os.getenv("MONGO_URL", "mongodb://localhost:27017")
            self.client = MongoClient(uri)
            self.db = self.client["sessions_store"]
            self.collection = self.db["messages"]
            logger.info("MongoDB connection established for SessionMessage")
        except errors.ConnectionFailure as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise

    def insert(self, message: SessionMessage) -> Tuple[bool, Any]:
        try:
            document = message.to_dict()
            result = self.collection.insert_one(document)
            logger.info(f"SessionMessage inserted with session_id: {message.session_id}")
            return True, result.inserted_id
        except errors.PyMongoError as e:
            logger.error(f"Error inserting SessionMessage: {e}")
            return False, str(e)

    def update(self, session_id: str, update_fields: Dict[str, Any]) -> Tuple[bool, Any]:
        try:
            result = self.collection.update_one(
                {"session_id": session_id},
                {"$set": update_fields},
                upsert=True
            )
            if result.modified_count > 0:
                logger.info(f"SessionMessage with session_id {session_id} updated")
                return True, result.modified_count
            else:
                logger.info(f"No document found with session_id {session_id} to update")
                return False, "No document found to update"
        except errors.PyMongoError as e:
            logger.error(f"Error updating SessionMessage: {e}")
            return False, str(e)

    def delete(self, session_id: str) -> Tuple[bool, Any]:
        try:
            result = self.collection.delete_one({"session_id": session_id})
            if result.deleted_count > 0:
                logger.info(f"SessionMessage with session_id {session_id} deleted")
                return True, result.deleted_count
            else:
                logger.info(f"No document found with session_id {session_id} to delete")
                return False, "No document found to delete"
        except errors.PyMongoError as e:
            logger.error(f"Error deleting SessionMessage: {e}")
            return False, str(e)

    def query(self, query_filter: Dict[str, Any]) -> Tuple[bool, Any]:
        try:
            result = self.collection.find(query_filter)
            documents = []
            for doc in result:
                doc.pop('_id', None)
                documents.append(doc)
            logger.info(f"Query successful, found {len(documents)} documents")
            return True, documents
        except errors.PyMongoError as e:
            logger.error(f"Error querying SessionMessages: {e}")
            return False, str(e)

    def get_by_session_id(self, session_id: str) -> Tuple[bool, Any]:
        try:
            doc = self.collection.find_one({"session_id": session_id})
            if doc:
                doc.pop('_id', None)
                message = SessionMessage.from_dict(doc)
                logger.info(f"SessionMessage with session_id {session_id} retrieved")
                return True, message
            else:
                logger.info(f"No SessionMessage found with session_id {session_id}")
                return False, "No document found"
        except errors.PyMongoError as e:
            logger.error(f"Error retrieving SessionMessage: {e}")
            return False, str(e)

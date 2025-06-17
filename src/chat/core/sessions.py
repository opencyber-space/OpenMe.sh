import os
import logging
from typing import Tuple, Dict, Any
from pymongo import MongoClient, errors
from dataclasses import asdict
from .schema import ChatSession, ChatMessage

logger = logging.getLogger(__name__)


class ChatSessionDatabase:
    def __init__(self):
        try:
            uri = os.getenv("MONGO_URL", "mongodb://localhost:27017")
            self.client = MongoClient(uri)
            self.db = self.client["chat_store"]
            self.collection = self.db["sessions"]
            logger.info("MongoDB connection established for ChatSession")
        except errors.ConnectionFailure as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise

    def insert(self, session: ChatSession) -> Tuple[bool, Any]:
        try:
            document = session.to_dict()
            result = self.collection.insert_one(document)
            logger.info(f"Chat session inserted with session_id: {session.session_id}")
            return True, result.inserted_id
        except errors.PyMongoError as e:
            logger.error(f"Error inserting ChatSession: {e}")
            return False, str(e)

    def update(self, session_id: str, update_fields: Dict[str, Any]) -> Tuple[bool, Any]:
        try:
            result = self.collection.update_one(
                {"session_id": session_id},
                {"$set": update_fields},
                upsert=True
            )
            if result.modified_count > 0:
                logger.info(f"Chat session with session_id {session_id} updated")
                return True, result.modified_count
            else:
                logger.info(f"No document found with session_id {session_id} to update")
                return False, "No document found to update"
        except errors.PyMongoError as e:
            logger.error(f"Error updating ChatSession: {e}")
            return False, str(e)

    def delete(self, session_id: str) -> Tuple[bool, Any]:
        try:
            result = self.collection.delete_one({"session_id": session_id})
            if result.deleted_count > 0:
                logger.info(f"Chat session with session_id {session_id} deleted")
                return True, result.deleted_count
            else:
                logger.info(f"No document found with session_id {session_id} to delete")
                return False, "No document found to delete"
        except errors.PyMongoError as e:
            logger.error(f"Error deleting ChatSession: {e}")
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
            logger.error(f"Error querying ChatSession: {e}")
            return False, str(e)

    def get_by_session_id(self, session_id: str) -> Tuple[bool, Any]:
        try:
            doc = self.collection.find_one({"session_id": session_id})
            if doc:
                doc.pop('_id', None)
                session = ChatSession.from_dict(doc)
                logger.info(f"Chat session with session_id {session_id} retrieved")
                return True, session
            else:
                logger.info(f"No ChatSession found with session_id {session_id}")
                return False, "No document found"
        except errors.PyMongoError as e:
            logger.error(f"Error retrieving ChatSession: {e}")
            return False, str(e)


class ChatMessagesDatabase:
    def __init__(self):
        try:
            uri = os.getenv("MONGO_URL", "mongodb://localhost:27017")
            self.client = MongoClient(uri)
            self.db = self.client["chat_store"]
            self.collection = self.db["messages"]
            logger.info("MongoDB connection established for ChatMessages")
        except errors.ConnectionFailure as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise

    def insert(self, message: ChatMessage) -> Tuple[bool, Any]:
        try:
            document = message.to_dict()
            result = self.collection.insert_one(document)
            logger.info(f"Chat message inserted with chat_id: {message.chat_id}")
            return True, result.inserted_id
        except errors.PyMongoError as e:
            logger.error(f"Error inserting ChatMessage: {e}")
            return False, str(e)

    def query_by_session(self, session_id: str) -> Tuple[bool, Any]:
        try:
            result = self.collection.find({"session_id": session_id}).sort("timestamp", 1)
            messages = []
            for doc in result:
                doc.pop("_id", None)
                messages.append(doc)
            logger.info(f"Found {len(messages)} messages for session_id: {session_id}")
            return True, messages
        except errors.PyMongoError as e:
            logger.error(f"Error querying messages: {e}")
            return False, str(e)

    def get_by_chat_id(self, chat_id: str) -> Tuple[bool, Any]:
        try:
            doc = self.collection.find_one({"chat_id": chat_id})
            if doc:
                doc.pop('_id', None)
                return True, ChatMessage.from_dict(doc)
            else:
                return False, "No document found"
        except errors.PyMongoError as e:
            logger.error(f"Error retrieving ChatMessage: {e}")
            return False, str(e)

    def delete_by_chat_id(self, chat_id: str) -> Tuple[bool, Any]:
        try:
            result = self.collection.delete_one({"chat_id": chat_id})
            if result.deleted_count > 0:
                logger.info(f"Deleted message with chat_id: {chat_id}")
                return True, result.deleted_count
            else:
                return False, "No document found to delete"
        except errors.PyMongoError as e:
            logger.error(f"Error deleting message: {e}")
            return False, str(e)
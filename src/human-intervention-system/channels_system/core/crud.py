import os
import logging
from pymongo import MongoClient, errors
from typing import Dict, Any, List, Tuple
from .schema import ChannelStoreObject 

logger = logging.getLogger(__name__)


class ChannelStoreDatabase:
    def __init__(self):
        try:
            uri = os.getenv("MONGO_URL", "mongodb://localhost:27017")
            self.client = MongoClient(uri)
            self.db = self.client["channel_store"]
            self.collection = self.db["channels"]
            logger.info("MongoDB connection established for ChannelStore")
        except errors.ConnectionFailure as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise

    def insert(self, channel: ChannelStoreObject) -> Tuple[bool, Any]:
        try:
            document = channel.to_dict()
            result = self.collection.insert_one(document)
            logger.info(f"Channel inserted with channel_id: {channel.channel_id}")
            return True, result.inserted_id
        except errors.PyMongoError as e:
            logger.error(f"Error inserting Channel: {e}")
            return False, str(e)

    def update(self, channel_id: str, update_fields: Dict[str, Any]) -> Tuple[bool, Any]:
        try:
            result = self.collection.update_one(
                {"channel_id": channel_id},
                {"$set": update_fields},
                upsert=True
            )
            if result.modified_count > 0:
                logger.info(f"Channel with channel_id {channel_id} updated")
                return True, result.modified_count
            else:
                logger.info(f"No document found with channel_id {channel_id} to update")
                return False, "No document found to update"
        except errors.PyMongoError as e:
            logger.error(f"Error updating Channel: {e}")
            return False, str(e)

    def delete(self, channel_id: str) -> Tuple[bool, Any]:
        try:
            result = self.collection.delete_one({"channel_id": channel_id})
            if result.deleted_count > 0:
                logger.info(f"Channel with channel_id {channel_id} deleted")
                return True, result.deleted_count
            else:
                logger.info(f"No document found with channel_id {channel_id} to delete")
                return False, "No document found to delete"
        except errors.PyMongoError as e:
            logger.error(f"Error deleting Channel: {e}")
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
            logger.error(f"Error querying Channels: {e}")
            return False, str(e)

    def get_by_channel_id(self, channel_id: str) -> Tuple[bool, Any]:
        try:
            doc = self.collection.find_one({"channel_id": channel_id})
            if doc:
                doc.pop('_id', None)
                channel = ChannelStoreObject.from_dict(doc)
                logger.info(f"Channel with channel_id {channel_id} retrieved")
                return True, channel
            else:
                logger.info(f"No Channel found with channel_id {channel_id}")
                return False, "No document found"
        except errors.PyMongoError as e:
            logger.error(f"Error retrieving Channel: {e}")
            return False, str(e)

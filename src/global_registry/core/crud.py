import os
import logging
from pymongo import MongoClient, errors
from typing import Dict, Any, Tuple, List
from .schema import BackboneDataObject  

logger = logging.getLogger(__name__)


class BackboneDataDatabase:
    def __init__(self):
        try:
            uri = os.getenv("MONGO_URL", "mongodb://localhost:27017")
            self.client = MongoClient(uri)
            self.db = self.client["backbone_registry"]
            self.collection = self.db["backbone_data"]
            logger.info("MongoDB connection established for BackboneData")
        except errors.ConnectionFailure as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise

    def insert(self, record: BackboneDataObject) -> Tuple[bool, Any]:
        try:
            document = record.to_dict()
            result = self.collection.insert_one(document)
            logger.info(f"Backbone record inserted with system_id: {record.system_id}")
            return True, result.inserted_id
        except errors.PyMongoError as e:
            logger.error(f"Error inserting BackboneData: {e}")
            return False, str(e)

    def update(self, system_id: str, update_fields: Dict[str, Any]) -> Tuple[bool, Any]:
        try:
            result = self.collection.update_one(
                {"system_id": system_id},
                {"$set": update_fields},
                upsert=True
            )
            if result.modified_count > 0:
                logger.info(f"BackboneData with system_id {system_id} updated")
                return True, result.modified_count
            else:
                logger.info(f"No document found with system_id {system_id} to update")
                return False, "No document found to update"
        except errors.PyMongoError as e:
            logger.error(f"Error updating BackboneData: {e}")
            return False, str(e)

    def delete(self, system_id: str) -> Tuple[bool, Any]:
        try:
            result = self.collection.delete_one({"system_id": system_id})
            if result.deleted_count > 0:
                logger.info(f"BackboneData with system_id {system_id} deleted")
                return True, result.deleted_count
            else:
                logger.info(f"No document found with system_id {system_id} to delete")
                return False, "No document found to delete"
        except errors.PyMongoError as e:
            logger.error(f"Error deleting BackboneData: {e}")
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
            logger.error(f"Error querying BackboneData: {e}")
            return False, str(e)

    def get_by_system_id(self, system_id: str) -> Tuple[bool, Any]:
        try:
            doc = self.collection.find_one({"system_id": system_id})
            if doc:
                doc.pop('_id', None)
                record = BackboneDataObject.from_dict(doc)
                logger.info(f"BackboneData with system_id {system_id} retrieved")
                return True, record
            else:
                logger.info(f"No BackboneData found with system_id {system_id}")
                return False, "No document found"
        except errors.PyMongoError as e:
            logger.error(f"Error retrieving BackboneData: {e}")
            return False, str(e)

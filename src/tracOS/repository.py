from pymongo import MongoClient, errors
from datetime import datetime
from src.config import MONGO_URI, DB_NAME, COLLECTION_NAME
from src.logger import logger
import time

class TracOSRepository:
    def __init__(self):
        retries = 3
        for attempt in range(retries):
            try:
                self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
                self.db = self.client[DB_NAME]
                self.collection = self.db[COLLECTION_NAME]
                self.client.admin.command("ping")
                break
            except errors.ServerSelectionTimeoutError as e:
                logger.error(f"Erro ao conectar com MongoDB (tentativa {attempt + 1}): {e}")
                time.sleep(2)
        else:
            raise Exception("Falha ao conectar com MongoDB após múltiplas tentativas")

    def upsert_workorder(self, workorder):
        self.collection.update_one(
            {"id": workorder["id"]},
            {"$set": workorder},
            upsert=True
        )

    def get_unsynced_workorders(self):
        return list(self.collection.find({"isSynced": False}))

    def mark_as_synced(self, workorder_id):
        self.collection.update_one(
            {"id": workorder_id},
            {"$set": {"isSynced": True, "syncedAt": datetime.utcnow().isoformat()}}
        )
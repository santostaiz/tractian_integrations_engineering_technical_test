from pymongo import MongoClient, errors
from datetime import datetime, timezone
from src.config import get_mongo_uri, DB_NAME, COLLECTION_NAME
from src.logger import logger
import time

class TracOSRepository:
    def __init__(self):
        retries = 3
        for attempt in range(retries):
            try:
                self.client = MongoClient(get_mongo_uri(), serverSelectionTimeoutMS=5000)
                self.db = self.client[DB_NAME]
                self.collection = self.db[COLLECTION_NAME]
                self.client.admin.command("ping")
                self.collection.create_index("id", unique=True)
                break
            except errors.ServerSelectionTimeoutError as e:
                logger.error(f"Erro ao conectar com MongoDB (tentativa {attempt + 1}): {e}")
                time.sleep(2)
        else:
            raise Exception("Falha ao conectar com MongoDB após múltiplas tentativas")

    def upsert_workorder(self, workorder):
        if "id" not in workorder or not workorder["id"]:
            logger.error(f"Tentativa de inserir ordem sem ID: {workorder}")
            return
        
        result = self.collection.update_one(
            {"id": workorder["id"]},
            {"$set": workorder},
            upsert=True
        )
        if result.upserted_id:
            logger.info(f"Ordem {workorder['id']} inserida.")
        else:
            logger.info(f"Ordem {workorder['id']} atualizada.")

    def get_unsynced_workorders(self):
        return list(self.collection.find({"isSynced": False}))

    def mark_as_synced(self, workorder_id):
        self.collection.update_one(
            {"id": workorder_id},
            {"$set": {"isSynced": True, "syncedAt": datetime.now(timezone.utc).isoformat()}}
        )
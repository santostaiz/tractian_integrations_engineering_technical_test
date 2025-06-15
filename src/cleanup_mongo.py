from pymongo import MongoClient
from src.config import MONGO_URI, DB_NAME, COLLECTION_NAME
from src.logger import logger


def cleanup_invalid_workorders():
    try:
        logger.info("🔍 Conectando ao MongoDB para limpeza...")
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Contagem inicial de documentos inválidos
        count_null_id = collection.count_documents({"id": None})
        count_missing_id = collection.count_documents({"id": {"$exists": False}})

        logger.info(f"Documentos com 'id': None → {count_null_id}")
        logger.info(f"Documentos sem campo 'id' → {count_missing_id}")

        # Deletar documentos com id: None
        result_null_id = collection.delete_many({"id": None})
        logger.info(f"Documentos deletados com 'id': None → {result_null_id.deleted_count}")

        # Deletar documentos sem campo 'id'
        result_missing_id = collection.delete_many({"id": {"$exists": False}})
        logger.info(f"Documentos deletados sem campo 'id' → {result_missing_id.deleted_count}")

        total_deleted = result_null_id.deleted_count + result_missing_id.deleted_count
        logger.info(f"Limpeza finalizada. Total de documentos removidos: {total_deleted}")

    except Exception as e:
        logger.critical(f"Erro durante a limpeza do MongoDB: {e}")


if __name__ == "__main__":
    cleanup_invalid_workorders()
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega automaticamente as variáveis do .env

MONGO_URI = os.getenv("MONGO_URI")
DATA_INBOUND_DIR = os.getenv("DATA_INBOUND_DIR")
DATA_OUTBOUND_DIR = os.getenv("DATA_OUTBOUND_DIR")
DB_NAME = "tractian"
COLLECTION_NAME = "workorders"
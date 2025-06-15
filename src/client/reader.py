import os
import json
from src.logger import logger

def load_client_workorders(input_dir):
    workorders = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(input_dir, filename)) as f:
                    data = json.load(f)
                    workorders.append(data)
            except Exception as e:
                logger.error(f"Erro ao ler arquivo {filename}: {e}")
    return workorders
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

def write_client_workorder(output_dir, filename, workorder):
    try:
        with open(os.path.join(output_dir, filename), "w") as f:
            json.dump(workorder, f, indent=2)
    except Exception as e:
        logger.error(f"Erro ao escrever arquivo {filename}: {e}")

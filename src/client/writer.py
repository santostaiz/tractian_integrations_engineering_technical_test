import os
import json
from src.logger import logger

def write_client_workorder(output_dir, filename, workorder):
    try:
        with open(os.path.join(output_dir, filename), "w") as f:
            json.dump(workorder, f, indent=2)
    except Exception as e:
        logger.error(f"Erro ao escrever arquivo {filename}: {e}")

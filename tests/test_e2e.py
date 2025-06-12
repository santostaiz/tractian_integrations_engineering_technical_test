from src.main import run_inbound, run_outbound
from src.tracOS.repository import TracOSRepository
import os
import json

def test_end_to_end_flow(tmp_path):
    repo = TracOSRepository()

    # Cria um arquivo de entrada simulado
    input_file = tmp_path / "test.json"
    input_data = {
        "id": "WO123",
        "status": "NEW",
        "createdAt": "2024-01-01T00:00:00"
    }
    with open(input_file, "w") as f:
        json.dump(input_data, f)

    # Configura variáveis de ambiente
    os.environ["DATA_INBOUND_DIR"] = str(tmp_path)
    os.environ["DATA_OUTBOUND_DIR"] = str(tmp_path)

    # Executa fluxo
    run_inbound(repo)
    run_outbound(repo)

    # Verifica saída
    output_file = tmp_path / "WO123.json"
    assert output_file.exists()

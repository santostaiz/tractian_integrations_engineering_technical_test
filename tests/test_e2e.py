import json
import pytest
from src.tracOS.repository import TracOSRepository
from src.main import run_inbound, run_outbound


@pytest.fixture
def repo():
    return TracOSRepository()


def test_end_to_end_flow(tmp_path, monkeypatch, repo):
    # Configura os diretórios temporários
    input_dir = tmp_path / "inbound"
    output_dir = tmp_path / "outbound"
    input_dir.mkdir()
    output_dir.mkdir()

    # Sobrescreve as variáveis de ambiente para os diretórios de teste
    monkeypatch.setenv("DATA_INBOUND_DIR", str(input_dir))
    monkeypatch.setenv("DATA_OUTBOUND_DIR", str(output_dir))

    # Cria um arquivo de entrada simulado no formato do CLIENTE
    input_file = input_dir / "test.json"
    input_data = {
        "orderNo": "123",
        "summary": "Teste de ordem",
        "creationDate": "2024-01-01T00:00:00",
        "lastUpdateDate": "2024-01-02T00:00:00",
        "isDone": False,
        "isDeleted": False
    }
    with open(input_file, "w") as f:
        json.dump(input_data, f)

    # Executa os fluxos
    run_inbound(repo)
    run_outbound(repo)

    # Verifica se o arquivo de saída foi criado corretamente
    output_file = output_dir / "123.json"
    assert output_file.exists(), "Arquivo de saída não foi gerado"

    # Verifica arquivo de saída
    with open(output_file) as f:
        output_data = json.load(f)

    assert output_data["orderNo"] == "123"
    assert output_data["summary"] == "Teste de ordem"
    assert output_data["creationDate"].startswith("2024-01-01")

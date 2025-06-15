from src.main import run_inbound
import json


def test_inbound_process(repo, tmp_path, monkeypatch):
    input_dir = tmp_path / "inbound"
    input_dir.mkdir()

    monkeypatch.setenv("DATA_INBOUND_DIR", str(input_dir))

    input_file = input_dir / "test.json"
    input_data = {
        "orderNo": "123",
        "summary": "Teste",
        "creationDate": "2024-01-01T00:00:00",
        "lastUpdateDate": "2024-01-02T00:00:00",
        "isDone": False,
        "isDeleted": False
    }
    with open(input_file, "w") as f:
        json.dump(input_data, f)

    run_inbound(repo)

    unsynced = repo.get_unsynced_workorders()
    assert any(wo["id"] == "123" for wo in unsynced)

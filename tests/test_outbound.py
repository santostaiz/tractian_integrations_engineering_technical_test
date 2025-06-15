from src.main import run_outbound
import os
import json


def test_outbound_process(repo, tmp_path, monkeypatch):
    output_dir = tmp_path / "outbound"
    output_dir.mkdir()

    monkeypatch.setenv("DATA_OUTBOUND_DIR", str(output_dir))

    workorder = {
        "id": "123",
        "status": "in_progress",
        "createdAt": "2024-01-01T00:00:00",
        "updatedAt": "2024-01-02T00:00:00",
        "isSynced": False
    }
    repo.upsert_workorder(workorder)

    run_outbound(repo)

    output_file = output_dir / "123.json"
    assert output_file.exists()
    with open(output_file) as f:
        data = json.load(f)
        assert data["orderNo"] == "123"

import json
from src.client.reader import load_client_workorders
from src.client.writer import write_client_workorder


def test_write_and_load_workorder(tmp_path):
    output_file = tmp_path / "test.json"
    workorder = {"id": "123", "status": "in_progress"}

    write_client_workorder(str(tmp_path), "test.json", workorder)
    assert output_file.exists()

    loaded = load_client_workorders(str(tmp_path))
    assert loaded[0]["id"] == "123"

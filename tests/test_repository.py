def test_upsert_and_get_unsynced(repo):
    workorder = {
        "id": "123",
        "status": "in_progress",
        "createdAt": "2024-01-01T00:00:00",
        "updatedAt": "2024-01-01T00:00:00",
        "isSynced": False
    }
    repo.upsert_workorder(workorder)
    unsynced = repo.get_unsynced_workorders()
    assert any(wo["id"] == "123" for wo in unsynced)

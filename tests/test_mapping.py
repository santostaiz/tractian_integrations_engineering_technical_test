from src.translator.mapping import client_to_tracos, tracos_to_client, normalize_date
from datetime import datetime

def test_client_to_tracos_translation():
    raw = {
        "orderNo": "123",
        "summary": "Teste",
        "creationDate": "2024-01-01T00:00:00",
        "lastUpdateDate": "2024-01-02T00:00:00",
        "isDone": True,
        "isDeleted": False
    }
    result = client_to_tracos(raw)
    assert result["id"] == "123"
    assert result["status"] == "completed"


def test_tracos_to_client_translation():
    doc = {
        "id": "123",
        "title": "Teste",
        "status": "completed",
        "createdAt": "2024-01-01T00:00:00",
        "updatedAt": "2024-01-02T00:00:00",
        "deleted": False,
        "deletedAt": None
    }
    result = tracos_to_client(doc)
    assert result["orderNo"] == "123"
    assert result["isDone"]


def test_normalize_date_valid():
    input_date = "2024-01-01T00:00:00"
    result = normalize_date(input_date)

    # Verifica se o resultado é uma string no formato ISO 8601
    try:
        parsed = datetime.fromisoformat(result)
    except ValueError:
        assert False, f"O resultado '{result}' não está no formato ISO 8601"

    assert parsed.year == 2024
    assert parsed.month == 1
    assert parsed.day == 1

    assert parsed.tzinfo is not None, "Timezone não está definido. A data deve estar em UTC."

    # Verifica se é UTC
    assert parsed.tzinfo.utcoffset(parsed).total_seconds() == 0, "A data não está em UTC."
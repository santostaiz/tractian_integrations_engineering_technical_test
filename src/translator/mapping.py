from datetime import datetime

STATUS_MAP = {
    "NEW": "created",
    "IN_PROGRESS": "in_progress",
    "DONE": "closed"
}

REVERSE_STATUS_MAP = {v: k for k, v in STATUS_MAP.items()}
def get_status_from_client(data: dict) -> str:
    if data.get("isDeleted"):
        return "cancelled"
    if data.get("isCanceled"):
        return "cancelled"
    if data.get("isDone"):
        return "completed"
    if data.get("isOnHold"):
        return "on_hold"
    if data.get("isPending"):
        return "pending"
    return "in_progress"  # valor padrão

def client_to_tracos(raw: dict) -> dict:
    """Traduz dados do sistema do cliente para o formato TracOS."""

    # Determina o status com base nos flags booleanos
    if raw.get("isDeleted"):
        status = "cancelled"
    elif raw.get("isCanceled"):
        status = "cancelled"
    elif raw.get("isDone"):
        status = "completed"
    elif raw.get("isOnHold"):
        status = "on_hold"
    elif raw.get("isPending"):
        status = "pending"
    else:
        status = "in_progress"

    return {
        "id": raw["orderNo"],
        "status": status,
        "title": raw["summary"],
        "createdAt": datetime.fromisoformat(raw["creationDate"]),
        "updatedAt": datetime.fromisoformat(raw["lastUpdateDate"]),
        "deleted": raw.get("isDeleted", False),
        "deletedAt": datetime.fromisoformat(raw["deletedDate"]) if raw.get("deletedDate") else None,
        "isSynced": False,
        "syncedAt": None
    }

def tracos_to_client(doc: dict) -> dict:
    """Traduz dados do TracOS para o formato do sistema do cliente."""

    # Mapeia o status inversamente para os flags booleanos
    status = doc.get("status", "")
    return {
        "orderNo": doc["id"],
        "summary": doc.get("title", ""),
        "creationDate": doc["createdAt"].isoformat(),
        "lastUpdateDate": doc["updatedAt"].isoformat(),
        "deletedDate": doc["deletedAt"].isoformat() if doc.get("deletedAt") else None,
        "isDeleted": doc.get("deleted", False),
        "isCanceled": status == "cancelled",
        "isDone": status == "completed",
        "isOnHold": status == "on_hold",
        "isPending": status == "pending",
        "isActive": status in ("pending", "in_progress", "on_hold"),
        "isSynced": True
    }
def normalize_date(date_str):
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.astimezone().isoformat()
    except Exception:
        return datetime.utcnow().isoformat()

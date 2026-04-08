"""DPDP Act 2023 compliance endpoints — data access, deletion, export.

Every Indian user has the right to:
1. Access their data
2. Delete their data
3. Export their data
"""

import json
import logging
from pathlib import Path

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter()

_DATA_DIR = Path(__file__).parents[5] / "data"


def _filter_by_user(filepath: Path, user_field: str, user_id: str) -> list[dict]:
    """Load JSON file and filter entries by user identifier."""
    if not filepath.exists():
        return []
    try:
        data = json.loads(filepath.read_text())
        return [d for d in data if d.get(user_field) == user_id]
    except Exception:
        return []


def _remove_by_user(filepath: Path, user_field: str, user_id: str) -> int:
    """Remove all entries by a user from a JSON file. Returns count removed."""
    if not filepath.exists():
        return 0
    try:
        data = json.loads(filepath.read_text())
        before = len(data)
        filtered = [d for d in data if d.get(user_field) != user_id]
        filepath.write_text(json.dumps(filtered, indent=2, default=str))
        return before - len(filtered)
    except Exception as e:
        logger.error(f"Failed to delete user data from {filepath}: {e}")
        return 0


@router.get("/data/{user_id}")
async def get_user_data(user_id: str):
    """DPDP Act — Right to Access. Returns all data associated with a user."""
    reviews = _filter_by_user(_DATA_DIR / "reviews.json", "user_id", user_id)
    feedback = _filter_by_user(_DATA_DIR / "feedback.json", "user_id", user_id)
    mileage = _filter_by_user(_DATA_DIR / "mileage_logs.json", "user_id", user_id)
    service = _filter_by_user(_DATA_DIR / "service_logs.json", "user_id", user_id)

    return {
        "user_id": user_id,
        "reviews": reviews,
        "feedback": feedback,
        "mileage_logs": mileage,
        "service_logs": service,
        "total_records": len(reviews) + len(feedback) + len(mileage) + len(service),
    }


@router.delete("/data/{user_id}")
async def delete_user_data(user_id: str):
    """DPDP Act — Right to Erasure. Deletes all data associated with a user."""
    deleted = {
        "reviews": _remove_by_user(_DATA_DIR / "reviews.json", "user_id", user_id),
        "feedback": _remove_by_user(_DATA_DIR / "feedback.json", "user_id", user_id),
        "mileage_logs": _remove_by_user(_DATA_DIR / "mileage_logs.json", "user_id", user_id),
        "service_logs": _remove_by_user(_DATA_DIR / "service_logs.json", "user_id", user_id),
    }

    total = sum(deleted.values())

    return {
        "user_id": user_id,
        "deleted": deleted,
        "total_deleted": total,
        "message": f"Deleted {total} records. Your data has been erased."
        if total > 0
        else "No data found for this user.",
    }


@router.get("/data/{user_id}/export")
async def export_user_data(user_id: str):
    """DPDP Act — Right to Data Portability. Exports all user data as JSON."""
    data = await get_user_data(user_id)
    data["export_format"] = "JSON"
    data["notice"] = (
        "This is a complete export of your data stored on RideShala. "
        "You can request deletion at DELETE /api/v1/privacy/data/{user_id}."
    )
    return data

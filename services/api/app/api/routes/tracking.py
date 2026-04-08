"""Mileage and service cost tracking endpoints.

Users log their actual fill-ups and service visits.
This crowd-sourced data powers the "real-world mileage" and
"real service cost" features that make RideShala different.

MVP: JSON file storage. Production: PostgreSQL.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter()

# MVP file stores
_DATA_DIR = Path(__file__).parents[5] / "data"
_MILEAGE_FILE = _DATA_DIR / "mileage_logs.json"
_SERVICE_FILE = _DATA_DIR / "service_logs.json"


def _load_json(filepath: Path) -> list[dict]:
    if filepath.exists():
        try:
            return json.loads(filepath.read_text())
        except Exception:
            return []
    return []


def _save_json(filepath: Path, data: list[dict]) -> None:
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(json.dumps(data, indent=2, default=str))
    except Exception as e:
        logger.warning(f"Could not save to {filepath}: {e}")


# ─── Mileage Tracking ──────────────────────────────────


class FillUpLog(BaseModel):
    """A single fuel fill-up entry."""

    bike_model: str = Field(..., min_length=2, max_length=100)
    odometer_km: int = Field(..., ge=0, le=500000)
    litres_filled: float = Field(..., gt=0, le=30)
    price_per_litre: float = Field(..., gt=0, le=200)
    city: str | None = Field(None, max_length=50)
    is_full_tank: bool = Field(True, description="Was this a full tank fill-up?")


@router.post("/mileage")
async def log_fillup(entry: FillUpLog):
    """Log a fuel fill-up to track real-world mileage."""
    logs = _load_json(_MILEAGE_FILE)

    new_entry = {
        "id": len(logs) + 1,
        "bike_model": entry.bike_model,
        "odometer_km": entry.odometer_km,
        "litres_filled": entry.litres_filled,
        "price_per_litre": entry.price_per_litre,
        "total_cost": round(entry.litres_filled * entry.price_per_litre, 2),
        "city": entry.city,
        "is_full_tank": entry.is_full_tank,
        "created_at": datetime.now().isoformat(),
    }

    logs.append(new_entry)
    _save_json(_MILEAGE_FILE, logs)

    return {"status": "logged", "entry_id": new_entry["id"]}


@router.get("/mileage/{bike_model}")
async def get_mileage_stats(bike_model: str):
    """Get aggregated real-world mileage stats for a bike model."""
    logs = _load_json(_MILEAGE_FILE)

    model_lower = bike_model.lower().replace("-", " ")
    bike_logs = [
        l for l in logs
        if model_lower in l.get("bike_model", "").lower().replace("-", " ")
    ]

    if len(bike_logs) < 2:
        return {
            "bike": bike_model,
            "total_entries": len(bike_logs),
            "avg_mileage_kpl": None,
            "message": "Need at least 2 fill-up entries to calculate mileage.",
        }

    # Sort by odometer and calculate kpl between consecutive full-tank entries
    full_tank = sorted(
        [l for l in bike_logs if l.get("is_full_tank")],
        key=lambda x: x["odometer_km"],
    )

    mileages = []
    for i in range(1, len(full_tank)):
        km_diff = full_tank[i]["odometer_km"] - full_tank[i - 1]["odometer_km"]
        litres = full_tank[i]["litres_filled"]
        if litres > 0 and km_diff > 0:
            mileages.append(round(km_diff / litres, 1))

    avg_mileage = round(sum(mileages) / len(mileages), 1) if mileages else None
    avg_cost = round(
        sum(l.get("total_cost", 0) for l in bike_logs) / len(bike_logs), 0
    ) if bike_logs else None

    return {
        "bike": bike_model,
        "total_entries": len(bike_logs),
        "calculated_entries": len(mileages),
        "avg_mileage_kpl": avg_mileage,
        "min_mileage_kpl": min(mileages) if mileages else None,
        "max_mileage_kpl": max(mileages) if mileages else None,
        "avg_fill_cost_inr": avg_cost,
        "source": f"Calculated from {len(mileages)} full-tank fill-ups on RideShala",
    }


# ─── Service Cost Tracking ─────────────────────────────


class ServiceLog(BaseModel):
    """A single service visit entry."""

    bike_model: str = Field(..., min_length=2, max_length=100)
    odometer_km: int = Field(..., ge=0, le=500000)
    total_cost_inr: int = Field(..., ge=0, le=100000)
    service_type: str = Field(
        ..., description="Type: regular, major, repair, tyre, chain, brake"
    )
    work_done: str = Field(..., min_length=5, max_length=500)
    dealer_or_local: str = Field("dealer", description="'dealer' or 'local'")
    city: str | None = Field(None, max_length=50)


@router.post("/service")
async def log_service(entry: ServiceLog):
    """Log a service visit to track real service costs."""
    logs = _load_json(_SERVICE_FILE)

    new_entry = {
        "id": len(logs) + 1,
        "bike_model": entry.bike_model,
        "odometer_km": entry.odometer_km,
        "total_cost_inr": entry.total_cost_inr,
        "service_type": entry.service_type,
        "work_done": entry.work_done,
        "dealer_or_local": entry.dealer_or_local,
        "city": entry.city,
        "created_at": datetime.now().isoformat(),
    }

    logs.append(new_entry)
    _save_json(_SERVICE_FILE, logs)

    return {"status": "logged", "entry_id": new_entry["id"]}


@router.get("/service/{bike_model}")
async def get_service_stats(bike_model: str):
    """Get aggregated service cost stats for a bike model."""
    logs = _load_json(_SERVICE_FILE)

    model_lower = bike_model.lower().replace("-", " ")
    bike_logs = [
        l for l in logs
        if model_lower in l.get("bike_model", "").lower().replace("-", " ")
    ]

    if not bike_logs:
        return {
            "bike": bike_model,
            "total_entries": 0,
            "avg_service_cost_inr": None,
            "message": "No service data yet. Be the first to contribute!",
        }

    costs = [l["total_cost_inr"] for l in bike_logs]
    by_type = {}
    for l in bike_logs:
        t = l.get("service_type", "other")
        by_type.setdefault(t, []).append(l["total_cost_inr"])

    return {
        "bike": bike_model,
        "total_entries": len(bike_logs),
        "avg_service_cost_inr": round(sum(costs) / len(costs)),
        "min_cost_inr": min(costs),
        "max_cost_inr": max(costs),
        "by_type": {
            t: {"avg": round(sum(c) / len(c)), "count": len(c)}
            for t, c in by_type.items()
        },
        "dealer_vs_local": {
            "dealer": len([l for l in bike_logs if l.get("dealer_or_local") == "dealer"]),
            "local": len([l for l in bike_logs if l.get("dealer_or_local") == "local"]),
        },
        "source": f"Aggregated from {len(bike_logs)} service logs on RideShala",
    }

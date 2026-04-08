"""Ride planning API endpoint.

Plans routes with fuel stops, weather, and safety tips.
Uses OSRM (free) for routing and Open-Meteo (free) for weather.
"""

import bleach
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.middleware.rate_limiter import rate_limit_check

router = APIRouter()

_rate_limit = Depends(rate_limit_check)


class RidePlanRequest(BaseModel):
    query: str = Field(..., min_length=5, max_length=500)
    bike_model: str | None = Field(None, max_length=100)


@router.post("")
async def plan_ride(request: RidePlanRequest, req: Request, _=_rate_limit):  # noqa: B008
    """Plan a ride with route, fuel stops, weather, and safety tips.

    Example: "Plan a ride from Bangalore to Coorg on my Meteor 350"

    Uses free services:
    - OSRM (BSD) for routing
    - Open-Meteo (open source) for weather
    - Bike specs from our database for fuel calculations
    """
    graph = getattr(req.app.state, "graph", None)

    if graph:
        try:
            bikes = [bleach.clean(request.bike_model, tags=[], strip=True)] if request.bike_model else []
            initial_state = {
                "messages": [{"role": "user", "content": bleach.clean(request.query, tags=[], strip=True)}],
                "intent": "ride_plan",
                "bikes_mentioned": bikes,
                "user_profile": None,
                "specs_data": None,
                "reviews_data": None,
                "mileage_data": None,
                "service_data": None,
                "research_result": None,
                "comparison_result": None,
                "safety_result": None,
                "finance_result": None,
                "ride_plan_result": None,
                "provider": "groq",
                "needs_clarification": False,
                "sources": [],
                "total_tokens": 0,
            }

            result = await graph.ainvoke(initial_state)

            response_text = ""
            for msg in reversed(result.get("messages", [])):
                if isinstance(msg, dict) and msg.get("role") == "assistant":
                    response_text = msg["content"]
                    break
                elif hasattr(msg, "content") and hasattr(msg, "type") and msg.type == "ai":
                    response_text = msg.content
                    break

            return {
                "plan": response_text or "Could not generate ride plan.",
                "sources": result.get("sources", []),
                "provider": result.get("provider", "unknown"),
            }

        except Exception as e:
            return {
                "plan": f"Ride planning temporarily unavailable: {e}",
                "sources": [],
                "provider": "error",
            }

    return {
        "plan": "AI agents are starting up. Try: 'Plan a ride from Bangalore to Coorg on Meteor 350'",
        "sources": [],
        "provider": "none",
    }

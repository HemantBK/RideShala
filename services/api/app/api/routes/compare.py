"""Bike comparison API endpoints.

Uses the LangGraph agent graph for AI-powered comparison with reasoning,
and the finance agent for Total Cost of Ownership calculations.
"""

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from packages.ai.agents.tools.calculators import calculate_emi, calculate_insurance, calculate_rto
from packages.ai.agents.tools.search_specs import search_bike_specs

router = APIRouter()


class CompareRequest(BaseModel):
    bikes: list[str] = Field(..., min_length=2, max_length=4)
    user_height_cm: int | None = Field(None, ge=100, le=220)
    user_city: str | None = None
    user_budget: int | None = Field(None, ge=0)


@router.post("")
async def compare_bikes(request: CompareRequest, req: Request):
    """AI-powered bike comparison with reasoning."""
    graph = getattr(req.app.state, "graph", None)

    if graph:
        try:
            initial_state = {
                "messages": [
                    {
                        "role": "user",
                        "content": f"Compare {' vs '.join(request.bikes)}"
                        + (f" for a {request.user_height_cm}cm rider" if request.user_height_cm else "")
                        + (f" in {request.user_city}" if request.user_city else "")
                        + (f" with budget Rs {request.user_budget}" if request.user_budget else ""),
                    }
                ],
                "intent": "compare",
                "bikes_mentioned": request.bikes,
                "user_profile": {
                    k: v
                    for k, v in {
                        "height_cm": request.user_height_cm,
                        "city": request.user_city,
                        "budget_inr": request.user_budget,
                    }.items()
                    if v is not None
                },
                "specs_data": None,
                "reviews_data": None,
                "mileage_data": None,
                "service_data": None,
                "research_result": None,
                "comparison_result": None,
                "safety_result": None,
                "finance_result": None,
                "ride_plan_result": None,
                "provider": "vllm",
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
                "bikes": request.bikes,
                "comparison": response_text or "Could not generate comparison.",
                "sources": result.get("sources", []),
                "provider": result.get("provider", "unknown"),
            }
        except Exception as e:
            return {
                "bikes": request.bikes,
                "comparison": f"Comparison temporarily unavailable: {e}",
                "sources": [],
                "provider": "error",
            }

    # Fallback: return spec data directly when graph not available
    specs = {}
    for bike_name in request.bikes:
        results = await search_bike_specs(model_name=bike_name)
        if results:
            specs[bike_name] = results[0]

    return {
        "bikes": request.bikes,
        "comparison": "AI comparison agents are starting up. Here are the raw specs.",
        "specs": specs,
        "sources": ["OEM published specifications"],
        "provider": "fallback",
    }


@router.post("/tco")
async def compare_tco(request: CompareRequest):
    """Total Cost of Ownership comparison.

    Uses real financial calculators with published government rate data.
    """
    tco_results = {}

    for bike_name in request.bikes:
        results = await search_bike_specs(model_name=bike_name)
        if not results:
            tco_results[bike_name] = {"error": f"Bike '{bike_name}' not found in database"}
            continue

        bike = results[0]
        price = bike.get("price_ex_showroom_inr", 0)
        cc = bike.get("engine_cc", 200)
        mileage = bike.get("mileage_claimed_kpl", 35)
        state = request.user_city or "Karnataka"

        rto = calculate_rto(price, state)
        insurance_y1 = calculate_insurance(price, cc, year=1)
        insurance_y2 = calculate_insurance(price, cc, year=2)
        emi = calculate_emi(price)

        # 5-year fuel cost estimate
        daily_km = 30
        annual_km = daily_km * 300
        petrol_price = 102.86  # IOCL Bangalore
        annual_fuel = int((annual_km / mileage) * petrol_price) if mileage > 0 else 0
        fuel_5yr = annual_fuel * 5

        # 5-year service estimate
        service_per_year = 3000 * 2  # ~2 services/year
        service_5yr = service_per_year * 5

        total_5yr = price + rto["rto_charge_inr"] + insurance_y1["total_premium_inr"] + (insurance_y2["total_premium_inr"] * 4) + fuel_5yr + service_5yr

        tco_results[bike_name] = {
            "bike": bike["name"],
            "brand": bike["brand"],
            "ex_showroom": price,
            "rto": rto,
            "insurance_year1": insurance_y1,
            "emi_36_months": emi,
            "fuel_5yr": fuel_5yr,
            "service_5yr": service_5yr,
            "total_5yr_tco": total_5yr,
            "monthly_cost": int(total_5yr / 60),
            "sources": [
                f"{bike['brand']} published price",
                f"{state} RTO rate ({rto['rate_pct']}%)",
                "IRDAI published tariff rates",
                f"IOCL fuel price (Rs {petrol_price}/L)",
            ],
        }

    return {
        "bikes": request.bikes,
        "tco": tco_results,
        "disclaimer": "This is an estimate for educational purposes only. Not financial advice.",
    }

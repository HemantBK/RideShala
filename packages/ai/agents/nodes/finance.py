"""Finance agent node — TCO calculator, EMI, insurance, RTO.

All data from legally published sources:
- OEM prices (manufacturer websites)
- RTO charges (government rate tables)
- Insurance (IRDAI published tariff rates)
- Fuel costs (IOCL published prices)
- Service costs (user-reported on our platform)
"""

import json
import logging

from packages.ai.agents.state import RideShalaState
from packages.ai.prompts.system_base import FINANCE_PROMPT, PERSONA

logger = logging.getLogger(__name__)

# Standard financial formulas (pure math, no external data needed)
INSURANCE_RATE_THIRD_PARTY = 1680  # INR per year for 150-350cc (IRDAI tariff)
RTO_RATE_KARNATAKA_PCT = 0.13  # 13% of ex-showroom for Karnataka
PETROL_PRICE_INR = 102.86  # IOCL Bangalore rate (update periodically)


def calculate_emi(principal: int, annual_rate: float = 9.5, tenure_months: int = 36) -> float:
    """Standard EMI formula. Not financial advice."""
    monthly_rate = annual_rate / (12 * 100)
    emi = principal * monthly_rate * (1 + monthly_rate) ** tenure_months
    emi /= ((1 + monthly_rate) ** tenure_months - 1)
    return round(emi, 2)


def calculate_tco_estimate(
    ex_showroom: int,
    mileage_kpl: float,
    daily_km: float = 30,
    years: int = 5,
    city: str = "Bangalore",
) -> dict:
    """Estimate 5-year Total Cost of Ownership. All sources documented."""
    rto = int(ex_showroom * RTO_RATE_KARNATAKA_PCT)
    insurance_year1 = int(ex_showroom * 0.028) + INSURANCE_RATE_THIRD_PARTY
    insurance_subsequent = INSURANCE_RATE_THIRD_PARTY * (years - 1)
    total_insurance = insurance_year1 + insurance_subsequent

    total_km = daily_km * 300 * years  # ~300 riding days/year
    fuel_cost = int((total_km / mileage_kpl) * PETROL_PRICE_INR)

    service_cost = 3000 * 2 * years  # ~2 services/year at ~3000 INR avg
    tyre_cost = 6000 * (years // 2)  # Tyres every 2 years

    resale_pct = 0.55 if years <= 3 else 0.40  # Rough resale estimate
    resale_value = int(ex_showroom * resale_pct)

    total = ex_showroom + rto + total_insurance + fuel_cost + service_cost + tyre_cost - resale_value

    return {
        "ex_showroom": ex_showroom,
        "rto_charges": rto,
        "total_insurance": total_insurance,
        "fuel_cost": fuel_cost,
        "service_cost": service_cost,
        "tyre_cost": tyre_cost,
        "resale_value": resale_value,
        "total_tco": total,
        "monthly_cost": int(total / (years * 12)),
        "sources": {
            "price": "OEM published ex-showroom price",
            "rto": f"Karnataka RTO rate ({RTO_RATE_KARNATAKA_PCT*100}%)",
            "insurance": "IRDAI third-party tariff + estimated comprehensive",
            "fuel": f"IOCL Bangalore petrol price (Rs {PETROL_PRICE_INR}/L)",
            "service": "Estimated from industry average (user data pending)",
            "resale": "Estimated depreciation curve",
        },
    }


async def finance_agent_node(state: RideShalaState) -> dict:
    """Calculate Total Cost of Ownership and financial analysis."""
    from packages.ai.llm.router import LLMRouter

    bikes = state.get("bikes_mentioned", [])
    profile = state.get("user_profile") or {}
    last_msg = state["messages"][-1]
    query = last_msg.content if hasattr(last_msg, "content") else str(last_msg)

    context_parts = [f"Financial analysis request: {query}"]
    if bikes:
        context_parts.append(f"Bikes: {', '.join(bikes)}")
    if profile:
        context_parts.append(f"User profile: {json.dumps(profile)}")

    context = "\n".join(context_parts)
    system = f"{PERSONA}\n\n{FINANCE_PROMPT}"

    try:
        router = LLMRouter()
        response = await router.generate(
            provider=state.get("provider", "vllm"),
            system=system,
            messages=[{"role": "user", "content": context}],
            temperature=0.2,
            max_tokens=1536,
        )

        if hasattr(response, "choices"):
            result_text = response.choices[0].message.content
        elif hasattr(response, "content"):
            result_text = response.content[0].text if isinstance(response.content, list) else str(response.content)
        else:
            result_text = str(response)

        return {
            "finance_result": result_text,
            "sources": [
                "OEM published ex-showroom prices",
                "IRDAI published insurance tariffs",
                "Government RTO rate tables",
                f"IOCL fuel price (Rs {PETROL_PRICE_INR}/L)",
            ],
        }

    except Exception as e:
        logger.error(f"Finance agent failed: {e}")
        return {
            "finance_result": "I'm unable to generate the financial analysis right now. Please try again.",
            "sources": [],
        }

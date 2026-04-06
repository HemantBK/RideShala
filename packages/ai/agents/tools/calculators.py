"""Financial calculator tools — pure math, no external data needed.

EMI, RTO, insurance, and TCO calculations using publicly available
rate tables and standard financial formulas.

DISCLAIMER: These are estimates for educational purposes only.
Not financial advice.
"""


def calculate_emi(
    principal: int,
    annual_rate: float = 9.5,
    tenure_months: int = 36,
) -> dict:
    """Calculate Equated Monthly Installment.

    Args:
        principal: Loan amount in INR.
        annual_rate: Annual interest rate (default 9.5%).
        tenure_months: Loan tenure in months (default 36).

    Returns:
        Dict with EMI amount, total payment, and total interest.
    """
    monthly_rate = annual_rate / (12 * 100)
    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = principal * monthly_rate * (1 + monthly_rate) ** tenure_months
        emi /= ((1 + monthly_rate) ** tenure_months - 1)

    total_payment = emi * tenure_months
    total_interest = total_payment - principal

    return {
        "emi_inr": round(emi),
        "total_payment_inr": round(total_payment),
        "total_interest_inr": round(total_interest),
        "annual_rate_pct": annual_rate,
        "tenure_months": tenure_months,
        "source": "Standard EMI formula (reducing balance method)",
    }


def calculate_rto(
    ex_showroom_price: int,
    state: str = "Karnataka",
) -> dict:
    """Calculate RTO registration charges.

    Source: State transport department published rate tables.

    Args:
        ex_showroom_price: Ex-showroom price in INR.
        state: Indian state (affects rate).

    Returns:
        Dict with RTO charge breakdown.
    """
    # Simplified RTO rates (source: state transport websites)
    rto_rates = {
        "Karnataka": 0.13,
        "Maharashtra": 0.12,
        "Tamil Nadu": 0.11,
        "Delhi": 0.08,
        "Kerala": 0.09,
        "Telangana": 0.13,
        "Uttar Pradesh": 0.08,
        "Gujarat": 0.06,
        "Rajasthan": 0.08,
        "West Bengal": 0.07,
    }

    rate = rto_rates.get(state, 0.10)
    rto_charge = int(ex_showroom_price * rate)

    return {
        "rto_charge_inr": rto_charge,
        "state": state,
        "rate_pct": rate * 100,
        "source": f"{state} transport department published rates",
    }


def calculate_insurance(
    ex_showroom_price: int,
    engine_cc: float,
    year: int = 1,
) -> dict:
    """Calculate insurance estimate.

    Source: IRDAI published third-party tariff rates + estimated comprehensive.

    Args:
        ex_showroom_price: Ex-showroom price in INR.
        engine_cc: Engine displacement in cc.
        year: Policy year (1 = first year, 2+ = renewal).

    Returns:
        Dict with insurance breakdown.
    """
    # IRDAI third-party tariff (2024-25)
    if engine_cc <= 75:
        tp_premium = 538
    elif engine_cc <= 150:
        tp_premium = 714
    elif engine_cc <= 350:
        tp_premium = 1366
    else:
        tp_premium = 2804

    # Comprehensive estimate (OD component)
    if year == 1:
        od_rate = 0.028  # ~2.8% of IDV
    else:
        depreciation = min(0.10 * year, 0.50)
        od_rate = 0.028 * (1 - depreciation)

    idv = int(ex_showroom_price * (1 - min(0.10 * (year - 1), 0.50)))
    od_premium = int(idv * od_rate)
    total = od_premium + tp_premium

    return {
        "total_premium_inr": total,
        "od_premium_inr": od_premium,
        "tp_premium_inr": tp_premium,
        "idv_inr": idv,
        "year": year,
        "source": "IRDAI published third-party tariff + estimated comprehensive OD",
    }

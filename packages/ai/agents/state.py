"""RideShala LangGraph state schema."""

from typing import Annotated, TypedDict

from langgraph.graph import add_messages


class UserProfile(TypedDict, total=False):
    """User context for personalized recommendations."""

    height_cm: int
    city: str
    budget_inr: int
    riding_style: str  # commuter, touring, sport, cruiser
    daily_km: float
    experience: str  # beginner, intermediate, experienced


class RideShalaState(TypedDict):
    """Central state passed through the LangGraph agent graph."""

    # Conversation
    messages: Annotated[list, add_messages]
    intent: str  # bike_search, compare, safety, tco, ride_plan, general_chat, clarify

    # User context
    user_profile: UserProfile | None
    bikes_mentioned: list[str]

    # Retrieved data (populated by agent nodes)
    specs_data: dict | None
    reviews_data: list | None
    mileage_data: dict | None
    service_data: dict | None

    # Agent outputs
    research_result: str | None
    comparison_result: str | None
    safety_result: str | None
    finance_result: str | None
    ride_plan_result: str | None

    # Routing and metadata
    provider: str  # vllm, claude, groq
    needs_clarification: bool
    sources: list[str]
    total_tokens: int

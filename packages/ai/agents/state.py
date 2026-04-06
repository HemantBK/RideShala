"""RideShala LangGraph state schema."""

from typing import Annotated, Optional, TypedDict

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
    user_profile: Optional[UserProfile]
    bikes_mentioned: list[str]

    # Retrieved data (populated by agent nodes)
    specs_data: Optional[dict]
    reviews_data: Optional[list]
    mileage_data: Optional[dict]
    service_data: Optional[dict]

    # Agent outputs
    research_result: Optional[str]
    comparison_result: Optional[str]
    safety_result: Optional[str]
    finance_result: Optional[str]
    ride_plan_result: Optional[str]

    # Routing and metadata
    provider: str  # vllm, claude, groq
    needs_clarification: bool
    sources: list[str]
    total_tokens: int

"""RideShala LangGraph orchestration graph.

This is the central nervous system of RideShala's AI features.
It routes user queries to the appropriate agent based on intent,
orchestrates data retrieval and LLM calls, and ensures every
response includes source citations and passes safety guardrails.
"""

from langgraph.graph import END, StateGraph

from packages.ai.agents.state import RideShalaState


def route_by_intent(state: RideShalaState) -> str:
    """Route to the appropriate agent based on classified intent."""
    intent = state.get("intent", "general_chat")

    routing_map = {
        "bike_search": "research",
        "compare": "compare",
        "safety": "safety_check",
        "tco": "finance",
        "ride_plan": "ride_plan",
        "general_chat": "synthesize",
        "clarify": "clarify",
    }

    return routing_map.get(intent, "synthesize")


def build_rideshala_graph() -> StateGraph:
    """Build and compile the RideShala agent orchestration graph.

    Graph structure:
        classify_intent
          ├── bike_search    -> research     -> synthesize -> guardrail -> END
          ├── compare        -> compare      -> synthesize -> guardrail -> END
          ├── safety         -> safety_check -> synthesize -> guardrail -> END
          ├── tco            -> finance      -> synthesize -> guardrail -> END
          ├── ride_plan      -> ride_plan    -> synthesize -> guardrail -> END
          ├── general_chat   -> synthesize   -> guardrail -> END
          └── clarify        -> END (ask user for more info)
    """
    # Lazy imports to avoid circular dependencies and allow
    # the package to be imported before all deps are installed
    from packages.ai.agents.nodes.classify_intent import classify_intent_node
    from packages.ai.agents.nodes.comparison import comparison_agent_node
    from packages.ai.agents.nodes.finance import finance_agent_node
    from packages.ai.agents.nodes.guardrail import guardrail_node
    from packages.ai.agents.nodes.research import research_agent_node
    from packages.ai.agents.nodes.ride_plan import ride_plan_agent_node
    from packages.ai.agents.nodes.safety import safety_agent_node
    from packages.ai.agents.nodes.synthesize import synthesize_node

    graph = StateGraph(RideShalaState)

    # Add all nodes
    graph.add_node("classify_intent", classify_intent_node)
    graph.add_node("clarify", _clarify_node)
    graph.add_node("research", research_agent_node)
    graph.add_node("compare", comparison_agent_node)
    graph.add_node("safety_check", safety_agent_node)
    graph.add_node("finance", finance_agent_node)
    graph.add_node("ride_plan", ride_plan_agent_node)
    graph.add_node("synthesize", synthesize_node)
    graph.add_node("guardrail", guardrail_node)

    # Entry point
    graph.set_entry_point("classify_intent")

    # Conditional routing from intent classifier
    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "research": "research",
            "compare": "compare",
            "safety_check": "safety_check",
            "finance": "finance",
            "ride_plan": "ride_plan",
            "synthesize": "synthesize",
            "clarify": "clarify",
        },
    )

    # All agent nodes flow to synthesize -> guardrail -> END
    for node in ["research", "compare", "safety_check", "finance", "ride_plan"]:
        graph.add_edge(node, "synthesize")

    graph.add_edge("synthesize", "guardrail")
    graph.add_edge("guardrail", END)
    graph.add_edge("clarify", END)

    return graph.compile()


async def _clarify_node(state: RideShalaState) -> dict:
    """Ask the user for clarification when intent is unclear."""
    return {
        "messages": [
            {
                "role": "assistant",
                "content": (
                    "I'd like to help you find the perfect bike! Could you tell me more about:\n"
                    "- What's your budget range?\n"
                    "- What kind of riding? (daily commute, weekend trips, touring)\n"
                    "- Any specific bikes you're considering?\n"
                    "- Your city (for pricing and dealer info)?"
                ),
            }
        ],
        "needs_clarification": True,
    }


# Compiled graph — import and invoke this
rideshala_graph = build_rideshala_graph()

"""Streaming AI chat endpoint using Server-Sent Events (SSE).

This is the main conversational interface. User messages are processed
through the LangGraph agent graph, which routes to the appropriate
agent (research, comparison, safety, finance) based on intent.
"""

import json
import logging

import bleach
from fastapi import APIRouter, Depends, Request

from app.middleware.rate_limiter import rate_limit_check
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    """Validated chat request from the user."""

    message: str = Field(..., min_length=1, max_length=2000)
    bike_models: list[str] = Field(default_factory=list, max_length=5)
    session_id: str | None = None

    @field_validator("message")
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        """Strip HTML tags to prevent XSS."""
        return bleach.clean(v, tags=[], strip=True)


@router.post("/stream")
async def chat_stream(request: ChatRequest, req: Request, _=Depends(rate_limit_check)):
    """Stream AI response via Server-Sent Events.

    The response is streamed token-by-token for a responsive chat UX.
    The final SSE event includes source citations and metadata.
    """

    async def event_generator():
        graph = getattr(req.app.state, "graph", None)

        if graph:
            # Process through LangGraph agent graph
            try:
                initial_state = {
                    "messages": [{"role": "user", "content": request.message}],
                    "intent": "",
                    "bikes_mentioned": request.bike_models,
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
                    "provider": "vllm",
                    "needs_clarification": False,
                    "sources": [],
                    "total_tokens": 0,
                }

                result = await graph.ainvoke(initial_state)

                # Extract the assistant's response
                messages = result.get("messages", [])
                response_text = ""
                for msg in reversed(messages):
                    if hasattr(msg, "content") and hasattr(msg, "type") and msg.type == "ai":
                        response_text = msg.content
                        break
                    elif isinstance(msg, dict) and msg.get("role") == "assistant":
                        response_text = msg["content"]
                        break

                if not response_text:
                    response_text = "I processed your request but couldn't generate a response. Please try again."

                # Stream word by word for responsive UX
                words = response_text.split()
                for i, word in enumerate(words):
                    token = word + (" " if i < len(words) - 1 else "")
                    yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"

                # Final event with metadata
                yield f"data: {json.dumps({'type': 'done', 'sources': result.get('sources', []), 'intent': result.get('intent', 'unknown'), 'tokens_used': result.get('total_tokens', 0), 'provider': result.get('provider', 'unknown')})}\n\n"

            except Exception as e:
                logger.error(f"LangGraph processing failed: {e}")
                error_msg = "I'm having trouble processing your request right now. Please try again."
                yield f"data: {json.dumps({'type': 'token', 'content': error_msg})}\n\n"
                yield f"data: {json.dumps({'type': 'done', 'sources': [], 'error': str(e)})}\n\n"

        else:
            # Fallback when LangGraph is not initialized
            fallback = (
                f"Thanks for your question: '{request.message}'. "
                f"The AI agents are starting up. Once connected, I'll use our "
                f"multi-agent system (research, comparison, safety, finance) "
                f"powered by vLLM and Claude to give you a personalized answer "
                f"with source citations."
            )
            for word in fallback.split():
                yield f"data: {json.dumps({'type': 'token', 'content': word + ' '})}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'sources': [], 'tokens_used': 0})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("")
async def chat_sync(request: ChatRequest, req: Request, _=Depends(rate_limit_check)):
    """Non-streaming chat endpoint for simpler clients."""
    graph = getattr(req.app.state, "graph", None)

    if graph:
        try:
            initial_state = {
                "messages": [{"role": "user", "content": request.message}],
                "intent": "",
                "bikes_mentioned": request.bike_models,
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
                "provider": "vllm",
                "needs_clarification": False,
                "sources": [],
                "total_tokens": 0,
            }

            result = await graph.ainvoke(initial_state)

            messages = result.get("messages", [])
            response_text = ""
            for msg in reversed(messages):
                if hasattr(msg, "content") and hasattr(msg, "type") and msg.type == "ai":
                    response_text = msg.content
                    break
                elif isinstance(msg, dict) and msg.get("role") == "assistant":
                    response_text = msg["content"]
                    break

            return {
                "response": response_text or "Could not generate a response.",
                "sources": result.get("sources", []),
                "intent": result.get("intent", "unknown"),
                "provider": result.get("provider", "unknown"),
                "tokens_used": result.get("total_tokens", 0),
            }

        except Exception as e:
            logger.error(f"Chat processing failed: {e}")
            return {
                "response": "I'm having trouble right now. Please try again.",
                "sources": [],
                "intent": "error",
                "provider": "none",
                "tokens_used": 0,
            }

    return {
        "response": f"AI agents are starting up. Your question: '{request.message}'",
        "sources": [],
        "intent": "pending",
        "provider": "none",
        "tokens_used": 0,
    }

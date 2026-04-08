"""Review moderation pipeline.

Checks user-submitted reviews for:
1. Plagiarism — reject if too similar to existing reviews
2. Toxicity — reject if contains hate speech, abuse, or spam
3. Quality — reject if too generic or low-effort

All checks are local Python logic — no paid APIs needed.
"""

import logging
import re

logger = logging.getLogger(__name__)

# Common spam patterns
SPAM_PATTERNS = [
    r"buy now",
    r"click here",
    r"www\.\S+\.com",
    r"http[s]?://",
    r"call \d{10}",
    r"whatsapp",
    r"telegram",
    r"discount",
    r"free offer",
]

# Toxic words (basic list — expand as needed)
TOXIC_WORDS = [
    "idiot", "stupid", "worst ever", "fraud", "scam", "cheat",
    "hate", "terrible company", "never buy",
]

# Known template phrases from competitor platforms (plagiarism detection)
KNOWN_TEMPLATES = [
    "i have been using this bike for",
    "this is my first review",
    "i bought this bike from",
    "overall i am satisfied with",
    "pros and cons of this bike",
]


def check_plagiarism(text: str, existing_reviews: list[dict]) -> dict:
    """Check if review text is too similar to existing reviews.

    Uses simple character-level similarity (Jaccard on word sets).
    No external API needed.
    """
    text_words = set(text.lower().split())

    for existing in existing_reviews:
        existing_words = set(existing.get("text", "").lower().split())
        if not existing_words:
            continue

        # Jaccard similarity
        intersection = text_words & existing_words
        union = text_words | existing_words
        similarity = len(intersection) / len(union) if union else 0

        if similarity > 0.85:
            return {
                "passed": False,
                "reason": "This review is too similar to an existing review on our platform.",
                "similarity": round(similarity, 2),
            }

    return {"passed": True, "similarity": 0.0}


def check_toxicity(text: str) -> dict:
    """Check for toxic/abusive content.

    Basic keyword matching. Production should use a proper
    toxicity model (e.g., detoxify — Apache 2.0, free).
    """
    text_lower = text.lower()

    for word in TOXIC_WORDS:
        if word in text_lower:
            return {
                "passed": False,
                "reason": f"Review contains potentially abusive language. "
                f"Please keep your review constructive and respectful.",
                "flagged_word": word,
            }

    return {"passed": True}


def check_spam(text: str) -> dict:
    """Check for spam patterns (links, phone numbers, promotions)."""
    text_lower = text.lower()

    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text_lower):
            return {
                "passed": False,
                "reason": "Review contains spam-like content (links, phone numbers, or promotions).",
                "pattern": pattern,
            }

    return {"passed": True}


def check_quality(text: str) -> dict:
    """Check if review meets minimum quality standards."""
    words = text.split()

    # Too short (even after passing Pydantic's 50-char min)
    if len(words) < 10:
        return {
            "passed": False,
            "reason": "Review is too short. Please share more details about your experience.",
        }

    # All caps (shouting)
    uppercase_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    if uppercase_ratio > 0.7 and len(text) > 20:
        return {
            "passed": False,
            "reason": "Please don't write in ALL CAPS. Use normal capitalization.",
        }

    # Too many repeated characters (e.g., "goooood bikeeeee")
    if re.search(r"(.)\1{5,}", text):
        return {
            "passed": False,
            "reason": "Review contains excessive repeated characters. Please write normally.",
        }

    return {"passed": True}


def moderate_review(text: str, existing_reviews: list[dict] | None = None) -> dict:
    """Run all moderation checks on a review.

    Returns:
        {
            "approved": True/False,
            "checks": {
                "plagiarism": {"passed": True/False, ...},
                "toxicity": {"passed": True/False, ...},
                "spam": {"passed": True/False, ...},
                "quality": {"passed": True/False, ...},
            },
            "reason": "..." (if rejected)
        }
    """
    existing = existing_reviews or []

    checks = {
        "plagiarism": check_plagiarism(text, existing),
        "toxicity": check_toxicity(text),
        "spam": check_spam(text),
        "quality": check_quality(text),
    }

    all_passed = all(c["passed"] for c in checks.values())

    result = {
        "approved": all_passed,
        "checks": checks,
    }

    if not all_passed:
        # Find first failing check
        for name, check in checks.items():
            if not check["passed"]:
                result["reason"] = check["reason"]
                break

    return result

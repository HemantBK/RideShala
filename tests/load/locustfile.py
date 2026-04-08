"""Load testing with Locust (MIT license, free).

Simulates concurrent users hitting all major endpoints.

Usage:
    pip install locust
    locust -f tests/load/locustfile.py --host http://localhost:8080

    Then open http://localhost:8089 to configure and start the test.
    Target: 100 concurrent users, p95 < 3s for chat, < 500ms for data APIs.
"""

import json
import random

from locust import HttpUser, between, task


SAMPLE_QUERIES = [
    "Best bike for Bangalore commute under 2L?",
    "Compare Meteor 350 vs CB350",
    "5'7, back pain, weekend trips, budget 2.5L",
    "Cheapest bike with dual channel ABS",
    "Is the Hunter 350 good for a tall rider?",
    "Best adventure bike under 3 lakh",
    "KTM 390 Duke vs Triumph Speed 400",
    "Plan a ride from Bangalore to Coorg on Meteor 350",
    "What is the service cost of Pulsar NS200?",
    "Best mileage bike for daily commute",
]

SAMPLE_BIKES = [
    "royal-enfield-meteor-350",
    "honda-cb350",
    "royal-enfield-hunter-350",
    "bajaj-pulsar-ns200",
    "tvs-apache-rtr-200-4v",
    "ktm-390-duke",
    "triumph-speed-400",
    "yamaha-r15-v4",
    "hero-xpulse-200-4v",
    "bajaj-dominar-400",
]

COMPARE_PAIRS = [
    ["Meteor 350", "CB350"],
    ["Hunter 350", "Speed 400"],
    ["Pulsar NS200", "Apache RTR 200"],
    ["KTM 390 Duke", "Dominar 400"],
    ["Himalayan 450", "Scrambler 400 X"],
]


class RideShalaUser(HttpUser):
    """Simulates a typical RideShala user browsing and chatting."""

    wait_time = between(1, 5)

    @task(3)
    def chat_sync(self):
        """Most common action: ask the AI a question."""
        self.client.post(
            "/api/v1/chat",
            json={"message": random.choice(SAMPLE_QUERIES)},
            name="/api/v1/chat",
        )

    @task(2)
    def list_bikes(self):
        """Browse the bike catalog."""
        self.client.get(
            "/api/v1/specs?limit=10",
            name="/api/v1/specs",
        )

    @task(2)
    def get_bike(self):
        """View a specific bike's specs."""
        slug = random.choice(SAMPLE_BIKES)
        self.client.get(
            f"/api/v1/specs/{slug}",
            name="/api/v1/specs/[slug]",
        )

    @task(1)
    def compare_bikes(self):
        """Compare two bikes."""
        pair = random.choice(COMPARE_PAIRS)
        self.client.post(
            "/api/v1/compare",
            json={"bikes": pair},
            name="/api/v1/compare",
        )

    @task(1)
    def compare_tco(self):
        """Get TCO comparison."""
        pair = random.choice(COMPARE_PAIRS)
        self.client.post(
            "/api/v1/compare/tco",
            json={"bikes": pair, "user_city": "Bangalore"},
            name="/api/v1/compare/tco",
        )

    @task(1)
    def get_reviews(self):
        """Read reviews for a bike."""
        slug = random.choice(SAMPLE_BIKES)
        self.client.get(
            f"/api/v1/reviews/{slug}",
            name="/api/v1/reviews/[bike]",
        )

    @task(1)
    def health_check(self):
        """Check service health."""
        self.client.get("/health/ready", name="/health/ready")

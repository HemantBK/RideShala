"""Ride planner agent node — route planning with fuel stops, weather, and safety.

All services are free and open source:
- OSRM (BSD) for routing
- Open-Meteo (open source, no API key) for weather
- OpenStreetMap + Nominatim (ODbL) for geocoding
- Bike fuel tank + mileage from our database for fuel stops
"""

import logging
import os

import httpx

from packages.ai.agents.state import RideShalaState
from packages.ai.prompts.system_base import PERSONA, RIDE_PLAN_PROMPT

logger = logging.getLogger(__name__)

OSRM_URL = os.getenv("OSRM_URL", "https://router.project-osrm.org")
OPEN_METEO_URL = os.getenv("OPEN_METEO_URL", "https://api.open-meteo.com/v1")
NOMINATIM_URL = os.getenv("NOMINATIM_URL", "https://nominatim.openstreetmap.org")


async def _geocode(place: str) -> dict | None:
    """Geocode a place name to lat/lon using Nominatim (free, no key)."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{NOMINATIM_URL}/search",
                params={"q": place, "format": "json", "limit": 1, "countrycodes": "in"},
                headers={"User-Agent": "RideShala/1.0"},
                timeout=10,
            )
            results = resp.json()
            if results:
                return {
                    "name": results[0].get("display_name", place),
                    "lat": float(results[0]["lat"]),
                    "lon": float(results[0]["lon"]),
                }
    except Exception as e:
        logger.warning(f"Geocoding failed for '{place}': {e}")
    return None


async def _get_route(origin: dict, destination: dict) -> dict | None:
    """Get route from OSRM (free, open source, no key)."""
    try:
        async with httpx.AsyncClient() as client:
            coords = f"{origin['lon']},{origin['lat']};{destination['lon']},{destination['lat']}"
            resp = await client.get(
                f"{OSRM_URL}/route/v1/driving/{coords}",
                params={"overview": "full", "geometries": "geojson", "steps": "true"},
                timeout=15,
            )
            data = resp.json()
            if data.get("code") == "Ok" and data.get("routes"):
                route = data["routes"][0]
                return {
                    "distance_km": round(route["distance"] / 1000, 1),
                    "duration_hours": round(route["duration"] / 3600, 1),
                    "geometry": route.get("geometry"),
                }
    except Exception as e:
        logger.warning(f"OSRM routing failed: {e}")
    return None


async def _get_weather(lat: float, lon: float) -> dict | None:
    """Get weather forecast from Open-Meteo (free, no API key needed)."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{OPEN_METEO_URL}/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
                    "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
                    "timezone": "Asia/Kolkata",
                    "forecast_days": 3,
                },
                timeout=10,
            )
            data = resp.json()
            current = data.get("current", {})
            daily = data.get("daily", {})
            return {
                "current_temp_c": current.get("temperature_2m"),
                "humidity_pct": current.get("relative_humidity_2m"),
                "wind_kmph": current.get("wind_speed_10m"),
                "weather_code": current.get("weather_code"),
                "forecast_3day": {
                    "dates": daily.get("time", []),
                    "max_temps": daily.get("temperature_2m_max", []),
                    "min_temps": daily.get("temperature_2m_min", []),
                    "rain_chance": daily.get("precipitation_probability_max", []),
                },
            }
    except Exception as e:
        logger.warning(f"Weather fetch failed: {e}")
    return None


def _calculate_fuel_stops(
    distance_km: float, tank_litres: float, mileage_kpl: float
) -> list[dict]:
    """Calculate where fuel stops are needed based on bike specs."""
    if mileage_kpl <= 0 or tank_litres <= 0:
        return []

    range_km = tank_litres * mileage_kpl * 0.85  # 85% usable tank (reserve buffer)
    stops = []
    km_covered = 0

    while km_covered + range_km < distance_km:
        km_covered += range_km
        stops.append({
            "at_km": round(km_covered, 0),
            "reason": f"Refuel (estimated range per tank: {round(range_km)} km)",
        })

    return stops


async def ride_plan_agent_node(state: RideShalaState) -> dict:
    """Plan a ride with route, fuel stops, weather, and safety tips."""
    from packages.ai.agents.tools.search_specs import search_bike_specs
    from packages.ai.llm.router import LLMRouter

    last_msg = state["messages"][-1]
    query = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
    bikes = state.get("bikes_mentioned", [])

    # Extract origin/destination from query (simple heuristic)
    # LLM will help interpret, but we try geocoding common patterns
    words = query.lower()
    origin_place = None
    dest_place = None

    for keyword in ["from", "starting"]:
        if keyword in words:
            idx = words.index(keyword)
            after = query[idx + len(keyword) :].strip().split(" to ")
            if len(after) >= 1:
                origin_place = after[0].strip().rstrip(",. ")
            if len(after) >= 2:
                dest_place = after[1].strip().split()[0:3]
                dest_place = " ".join(dest_place).rstrip(",. ")
            break

    if not origin_place and " to " in words:
        parts = query.split(" to ", 1)
        # Take last few words before "to" as origin
        origin_words = parts[0].strip().split()[-3:]
        origin_place = " ".join(origin_words)
        dest_words = parts[1].strip().split()[:3]
        dest_place = " ".join(dest_words).rstrip(",. ")

    # Gather real data
    context_parts = [f"Ride planning request: {query}"]
    sources = []

    # 1. Route
    route_info = None
    if origin_place and dest_place:
        origin = await _geocode(origin_place)
        dest = await _geocode(dest_place)
        if origin and dest:
            route_info = await _get_route(origin, dest)
            if route_info:
                context_parts.append(
                    f"\n--- ROUTE DATA (from OSRM, free open source) ---\n"
                    f"From: {origin['name']}\n"
                    f"To: {dest['name']}\n"
                    f"Distance: {route_info['distance_km']} km\n"
                    f"Estimated time: {route_info['duration_hours']} hours"
                )
                sources.append("Route from OSRM (open source)")

            # 2. Weather at destination
            weather = await _get_weather(dest["lat"], dest["lon"])
            if weather:
                context_parts.append(
                    f"\n--- WEATHER AT DESTINATION (from Open-Meteo, free) ---\n"
                    f"Current: {weather['current_temp_c']}°C, "
                    f"Humidity: {weather['humidity_pct']}%, "
                    f"Wind: {weather['wind_kmph']} km/h\n"
                    f"3-day forecast rain chance: {weather['forecast_3day']['rain_chance']}"
                )
                sources.append("Weather from Open-Meteo (open source, no API key)")

    # 3. Fuel stops based on bike specs
    if bikes and route_info:
        results = await search_bike_specs(model_name=bikes[0])
        if results:
            bike = results[0]
            tank = bike.get("fuel_tank_litres", 0)
            mileage = bike.get("mileage_claimed_kpl", 0)
            fuel_stops = _calculate_fuel_stops(route_info["distance_km"], tank, mileage)

            context_parts.append(
                f"\n--- FUEL PLANNING ---\n"
                f"Bike: {bike['brand']} {bike['name']}\n"
                f"Tank: {tank}L | Mileage: {mileage} kpl (claimed)\n"
                f"Estimated range: {round(tank * mileage * 0.85)} km (85% usable)\n"
                f"Fuel stops needed: {len(fuel_stops)}"
            )
            for stop in fuel_stops:
                context_parts.append(f"  - Stop at ~{stop['at_km']} km: {stop['reason']}")
            sources.append(f"{bike['brand']} {bike['name']} specs from {bike.get('source_url', 'OEM')}")

    context = "\n".join(context_parts)
    system = f"{PERSONA}\n\n{RIDE_PLAN_PROMPT}"

    # 4. Call LLM to synthesize ride plan
    try:
        router = LLMRouter()
        response = await router.generate(
            provider=state.get("provider", "vllm"),
            system=system,
            messages=[{"role": "user", "content": context}],
            temperature=0.3,
            max_tokens=1024,
        )

        if hasattr(response, "choices"):
            result_text = response.choices[0].message.content
        elif hasattr(response, "content"):
            result_text = (
                response.content[0].text
                if isinstance(response.content, list)
                else str(response.content)
            )
        else:
            result_text = str(response)

        tokens = getattr(response, "usage", None)
        token_count = 0
        if tokens:
            token_count = getattr(tokens, "prompt_tokens", 0) + getattr(tokens, "completion_tokens", 0)

        return {
            "ride_plan_result": result_text,
            "sources": sources,
            "total_tokens": state.get("total_tokens", 0) + token_count,
        }

    except Exception as e:
        logger.error(f"Ride plan LLM failed: {e}")
        # Fallback: return raw data without LLM
        if route_info:
            fallback = (
                f"**Route:** {route_info['distance_km']} km, ~{route_info['duration_hours']} hours\n"
            )
            if fuel_stops:
                fallback += f"**Fuel stops:** {len(fuel_stops)} needed\n"
            fallback += "\n_AI ride planning tips unavailable. Try again shortly._"
            return {"ride_plan_result": fallback, "sources": sources}

        return {
            "ride_plan_result": "I need a start and destination to plan your ride. "
            "Try: 'Plan a ride from Bangalore to Coorg on my Meteor 350'",
            "sources": [],
        }

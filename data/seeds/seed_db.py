"""Seed the PostgreSQL database with initial bike data.

Usage:
    cd services/api
    PYTHONPATH=. python ../../data/seeds/seed_db.py

Loads bikes_india_top30.json into the bikes table.
Requires DATABASE_URL environment variable or uses default.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

import asyncpg


SEED_FILE = Path(__file__).parent / "bikes_india_top30.json"

DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://rideshala:rideshala@localhost:5432/rideshala",
)

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS bikes (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    engine_cc REAL,
    power_bhp REAL,
    torque_nm REAL,
    cylinders INTEGER,
    cooling VARCHAR(30),
    weight_kg REAL,
    seat_height_mm INTEGER,
    ground_clearance_mm INTEGER,
    fuel_tank_litres REAL,
    wheelbase_mm INTEGER,
    abs_type VARCHAR(30),
    traction_control BOOLEAN DEFAULT FALSE,
    riding_modes INTEGER DEFAULT 0,
    price_ex_showroom_inr INTEGER,
    price_source_url VARCHAR(500),
    gears INTEGER,
    transmission_type VARCHAR(30),
    top_speed_kmph INTEGER,
    mileage_claimed_kpl REAL,
    year INTEGER,
    is_electric BOOLEAN DEFAULT FALSE,
    source_url VARCHAR(500),
    avg_mileage_real_kpl REAL,
    avg_service_cost_inr INTEGER,
    total_reviews INTEGER DEFAULT 0,
    avg_rating REAL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
"""

INSERT_SQL = """
INSERT INTO bikes (
    slug, name, brand, category, engine_cc, power_bhp, torque_nm,
    cylinders, cooling, weight_kg, seat_height_mm, ground_clearance_mm,
    fuel_tank_litres, wheelbase_mm, abs_type, traction_control,
    riding_modes, price_ex_showroom_inr, gears, transmission_type,
    top_speed_kmph, mileage_claimed_kpl, year, is_electric, source_url
) VALUES (
    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14,
    $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25
)
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    price_ex_showroom_inr = EXCLUDED.price_ex_showroom_inr,
    updated_at = NOW();
"""


async def seed():
    """Load seed data into PostgreSQL."""
    print(f"Connecting to database...")
    conn = await asyncpg.connect(DB_URL)

    print("Creating bikes table if not exists...")
    await conn.execute(CREATE_TABLE_SQL)

    print(f"Loading seed data from {SEED_FILE}...")
    bikes = json.loads(SEED_FILE.read_text())

    count = 0
    for bike in bikes:
        await conn.execute(
            INSERT_SQL,
            bike["slug"],
            bike["name"],
            bike["brand"],
            bike["category"],
            bike.get("engine_cc"),
            bike.get("power_bhp"),
            bike.get("torque_nm"),
            bike.get("cylinders"),
            bike.get("cooling"),
            bike.get("weight_kg"),
            bike.get("seat_height_mm"),
            bike.get("ground_clearance_mm"),
            bike.get("fuel_tank_litres"),
            bike.get("wheelbase_mm"),
            bike.get("abs_type"),
            bike.get("traction_control", False),
            bike.get("riding_modes", 0),
            bike.get("price_ex_showroom_inr"),
            bike.get("gears"),
            bike.get("transmission_type"),
            bike.get("top_speed_kmph"),
            bike.get("mileage_claimed_kpl"),
            bike.get("year"),
            bike.get("is_electric", False),
            bike.get("source_url"),
        )
        count += 1

    await conn.close()
    print(f"Seeded {count} bikes successfully.")


if __name__ == "__main__":
    asyncio.run(seed())

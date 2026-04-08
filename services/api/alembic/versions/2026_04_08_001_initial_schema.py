"""Initial database schema — bikes, reviews, usage_logs, consent_logs.

Revision ID: 001
Revises: None
Create Date: 2026-04-08
"""

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "bikes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("brand", sa.String(100), nullable=False),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("engine_cc", sa.Float(), nullable=True),
        sa.Column("power_bhp", sa.Float(), nullable=True),
        sa.Column("torque_nm", sa.Float(), nullable=True),
        sa.Column("cylinders", sa.Integer(), nullable=True),
        sa.Column("cooling", sa.String(30), nullable=True),
        sa.Column("weight_kg", sa.Float(), nullable=True),
        sa.Column("seat_height_mm", sa.Integer(), nullable=True),
        sa.Column("ground_clearance_mm", sa.Integer(), nullable=True),
        sa.Column("fuel_tank_litres", sa.Float(), nullable=True),
        sa.Column("wheelbase_mm", sa.Integer(), nullable=True),
        sa.Column("abs_type", sa.String(30), nullable=True),
        sa.Column("traction_control", sa.Boolean(), server_default="false"),
        sa.Column("riding_modes", sa.Integer(), server_default="0"),
        sa.Column("price_ex_showroom_inr", sa.Integer(), nullable=True),
        sa.Column("price_source_url", sa.String(500), nullable=True),
        sa.Column("gears", sa.Integer(), nullable=True),
        sa.Column("transmission_type", sa.String(30), nullable=True),
        sa.Column("top_speed_kmph", sa.Integer(), nullable=True),
        sa.Column("mileage_claimed_kpl", sa.Float(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column("is_electric", sa.Boolean(), server_default="false"),
        sa.Column("available_colors", sa.Text(), nullable=True),
        sa.Column("source_url", sa.String(500), nullable=True),
        sa.Column("avg_mileage_real_kpl", sa.Float(), nullable=True),
        sa.Column("avg_service_cost_inr", sa.Integer(), nullable=True),
        sa.Column("total_reviews", sa.Integer(), server_default="0"),
        sa.Column("avg_rating", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("verified_by", sa.String(100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index("ix_bikes_brand", "bikes", ["brand"])
    op.create_index("ix_bikes_slug", "bikes", ["slug"])

    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("bike_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.String(100), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("rating", sa.Float(), nullable=False),
        sa.Column("aspect_ratings", sa.Text(), nullable=True),
        sa.Column("ownership_months", sa.Integer(), nullable=True),
        sa.Column("total_km", sa.Integer(), nullable=True),
        sa.Column("mileage_kpl", sa.Float(), nullable=True),
        sa.Column("last_service_cost_inr", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(20), server_default="pending"),
        sa.Column("is_verified_owner", sa.Boolean(), server_default="false"),
        sa.Column("consent_granted", sa.Boolean(), nullable=False),
        sa.Column("consent_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_original_content", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reviews_bike_id", "reviews", ["bike_id"])
    op.create_index("ix_reviews_user_id", "reviews", ["user_id"])

    op.create_table(
        "usage_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("provider", sa.String(20), nullable=False),
        sa.Column("model", sa.String(100), nullable=False),
        sa.Column("input_tokens", sa.Integer(), nullable=False),
        sa.Column("output_tokens", sa.Integer(), nullable=False),
        sa.Column("feature", sa.String(30), nullable=False),
        sa.Column("cost_usd", sa.Float(), nullable=False),
        sa.Column("user_id", sa.String(100), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_usage_logs_provider", "usage_logs", ["provider"])
    op.create_index("ix_usage_logs_timestamp", "usage_logs", ["timestamp"])

    op.create_table(
        "consent_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(100), nullable=False),
        sa.Column("purpose", sa.String(50), nullable=False),
        sa.Column("granted", sa.Boolean(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_consent_logs_user_id", "consent_logs", ["user_id"])


def downgrade() -> None:
    op.drop_table("consent_logs")
    op.drop_table("usage_logs")
    op.drop_table("reviews")
    op.drop_table("bikes")

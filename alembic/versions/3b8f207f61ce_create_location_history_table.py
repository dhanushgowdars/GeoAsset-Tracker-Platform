"""create_location_history_table

Revision ID: 3b8f207f61ce
Revises: 8cbc7bc1d5ef
Create Date: 2026-07-24 20:20:13.348969

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2

# revision identifiers, used by Alembic.
revision: str = "3b8f207f61ce"
down_revision: Union[str, Sequence[str], None] = "8cbc7bc1d5ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "location_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column(
            "location",
            geoalchemy2.types.Geometry(
                geometry_type="POINT",
                srid=4326,
                dimension=2,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "recorded_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["assets.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


    op.create_index(
        op.f("ix_location_history_asset_id"),
        "location_history",
        ["asset_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_location_history_id"),
        "location_history",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_location_history_id"),
        table_name="location_history",
    )

    op.drop_index(
        op.f("ix_location_history_asset_id"),
        table_name="location_history",
    )

    op.drop_table("location_history")
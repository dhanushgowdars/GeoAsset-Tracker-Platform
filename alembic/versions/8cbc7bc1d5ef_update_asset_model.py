"""update asset model

Revision ID: 8cbc7bc1d5ef
Revises: 3b143e5e21b1
Create Date: 2026-07-24 15:29:05.956913

"""

from typing import Sequence, Union

import geoalchemy2
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "8cbc7bc1d5ef"
down_revision: Union[str, Sequence[str], None] = "3b143e5e21b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    asset_type_enum = sa.Enum(
        "DRONE",
        "VEHICLE",
        "CAMERA",
        "SENSOR",
        "INFRASTRUCTURE",
        "OTHER",
        name="asset_type_enum",
    )
    asset_type_enum.create(op.get_bind(), checkfirst=True)

    asset_status_enum = sa.Enum(
        "ONLINE",
        "OFFLINE",
        "MAINTENANCE",
        "RETIRED",
        name="asset_status_enum",
    )
    asset_status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "assets",
        sa.Column("serial_number", sa.String(length=20), nullable=True),
    )

    op.add_column(
        "assets",
        sa.Column("asset_type", asset_type_enum, nullable=True),
    )

    op.add_column(
        "assets",
        sa.Column("status", asset_status_enum, nullable=True),
    )

    op.add_column(
        "assets",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.add_column(
        "assets",
        sa.Column(
            "last_location_update",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.add_column(
        "assets",
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.alter_column(
        "assets",
        "location",
        existing_type=geoalchemy2.types.Geometry(
            geometry_type="POINT",
            srid=4326,
            dimension=2,
            spatial_index=False,
            from_text="ST_GeomFromEWKT",
            name="geometry",
            _spatial_index_reflected=True,
        ),
        nullable=False,
    )

    op.alter_column(
        "assets",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )

    op.create_index(
        "idx_assets_location",
        "assets",
        ["location"],
        unique=False,
        postgresql_using="gist",
    )

    op.create_index(
        op.f("ix_assets_serial_number"),
        "assets",
        ["serial_number"],
        unique=True,
    )

    op.alter_column(
        "users",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "users",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )

    op.drop_index(op.f("ix_assets_serial_number"), table_name="assets")
    op.drop_index(
        "idx_assets_location",
        table_name="assets",
        postgresql_using="gist",
    )

    op.alter_column(
        "assets",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )

    op.alter_column(
        "assets",
        "location",
        existing_type=geoalchemy2.types.Geometry(
            geometry_type="POINT",
            srid=4326,
            dimension=2,
            spatial_index=False,
            from_text="ST_GeomFromEWKT",
            name="geometry",
            _spatial_index_reflected=True,
        ),
        nullable=True,
    )

    op.drop_column("assets", "deleted_at")
    op.drop_column("assets", "last_location_update")
    op.drop_column("assets", "updated_at")
    op.drop_column("assets", "status")
    op.drop_column("assets", "asset_type")
    op.drop_column("assets", "serial_number")

    asset_status_enum = sa.Enum(
        "ONLINE",
        "OFFLINE",
        "MAINTENANCE",
        "RETIRED",
        name="asset_status_enum",
    )
    asset_status_enum.drop(op.get_bind(), checkfirst=True)

    asset_type_enum = sa.Enum(
        "DRONE",
        "VEHICLE",
        "CAMERA",
        "SENSOR",
        "INFRASTRUCTURE",
        "OTHER",
        name="asset_type_enum",
    )
    asset_type_enum.drop(op.get_bind(), checkfirst=True)
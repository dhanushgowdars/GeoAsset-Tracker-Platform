"""add_postgis_location

Revision ID: 3b143e5e21b1
Revises: 46922a6b1160
Create Date: 2026-07-17 22:13:29.455990
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2

# revision identifiers, used by Alembic.
revision: str = "3b143e5e21b1"
down_revision: Union[str, Sequence[str], None] = "46922a6b1160"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "assets",
        sa.Column(
            "location",
            geoalchemy2.Geometry(
                geometry_type="POINT",
                srid=4326,
                spatial_index=False,
            ),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("assets", "location")

"""add_role_to_users

Revision ID: 46922a6b1160
Revises: 6276557cc0d1
Create Date: 2026-07-17 19:39:13.796704

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "46922a6b1160"
down_revision: Union[str, Sequence[str], None] = "6276557cc0d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Create PostgreSQL ENUM type
    user_role = sa.Enum(
        "USER",
        "ADMIN",
        name="userrole",
    )

    user_role.create(
        op.get_bind(),
        checkfirst=True,
    )

    # Add role column with default value for existing users
    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role,
            nullable=False,
            server_default="USER",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Remove the role column
    op.drop_column("users", "role")

    # Remove PostgreSQL ENUM type
    user_role = sa.Enum(
        "USER",
        "ADMIN",
        name="userrole",
    )

    user_role.drop(
        op.get_bind(),
        checkfirst=True,
    )

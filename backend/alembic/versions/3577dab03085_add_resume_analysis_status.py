"""add resume analysis status

Revision ID: 3577dab03085
Revises: 2447e249b535
Create Date: 2026-08-20 17:02:32.680198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3577dab03085'
down_revision: Union[str, Sequence[str], None] = '2447e249b535'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    analysis_status = sa.Enum(
        "PENDING",
        "ANALYZING",
        "COMPLETED",
        "FAILED",
        name="analysisstatus",
    )

    analysis_status.create(op.get_bind(), checkfirst=True)

    with op.batch_alter_table("resume_analyses") as batch_op:

        batch_op.add_column(
            sa.Column(
                "status",
                analysis_status,
                nullable=False,
                server_default="PENDING",
            )
        )

        batch_op.alter_column(
            "summary",
            existing_type=sa.VARCHAR(),
            nullable=True,
        )

        batch_op.alter_column(
            "skills",
            existing_type=sa.JSON(),
            nullable=True,
        )

        batch_op.alter_column(
            "education",
            existing_type=sa.JSON(),
            nullable=True,
        )

def downgrade() -> None:
    with op.batch_alter_table("resume_analyses") as batch_op:

        batch_op.alter_column(
            "education",
            existing_type=sa.JSON(),
            nullable=False,
        )

        batch_op.alter_column(
            "skills",
            existing_type=sa.JSON(),
            nullable=False,
        )

        batch_op.alter_column(
            "summary",
            existing_type=sa.VARCHAR(),
            nullable=False,
        )

        batch_op.drop_column("status")

    analysis_status = sa.Enum(
        "PENDING",
        "ANALYZING",
        "COMPLETED",
        "FAILED",
        name="analysisstatus",
    )

    analysis_status.drop(op.get_bind(), checkfirst=True)
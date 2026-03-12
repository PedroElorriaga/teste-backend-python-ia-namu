"""create recommendation feedbacks table

Revision ID: 8f3c2b1d4e5a
Revises: 6b9b7d1a1f2c
Create Date: 2026-03-11 17:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f3c2b1d4e5a'
down_revision: Union[str, Sequence[str], None] = '6b9b7d1a1f2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'recommendation_feedbacks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('recommendation_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('comment', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(
            ['recommendation_id'],
            ['recommendations.id'],
            name='fk_recommendation_feedbacks_recommendation_id_recommendations',
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('recommendation_feedbacks')
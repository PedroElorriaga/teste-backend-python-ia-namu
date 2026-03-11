"""new_table_recommendations

Revision ID: 22c4446398f9
Revises: 
Create Date: 2026-03-11 12:14:03.816683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '22c4446398f9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'recommendations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.Column('duration', sa.Float(), nullable=False),
        sa.Column('category', sa.String(length=64), nullable=False),
        sa.Column('reasoning', sa.String(length=255), nullable=False),
        sa.Column('precautions', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('recommendations')

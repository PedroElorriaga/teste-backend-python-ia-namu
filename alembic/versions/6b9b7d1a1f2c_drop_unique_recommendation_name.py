"""drop unique constraint on recommendation name

Revision ID: 6b9b7d1a1f2c
Revises: 4c2161973976
Create Date: 2026-03-11 17:10:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '6b9b7d1a1f2c'
down_revision: Union[str, Sequence[str], None] = '4c2161973976'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('recommendations_name_key', 'recommendations', type_='unique')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_unique_constraint('recommendations_name_key', 'recommendations', ['name'])

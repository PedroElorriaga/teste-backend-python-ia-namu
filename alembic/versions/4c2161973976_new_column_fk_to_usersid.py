"""new_column_FK_to_usersId

Revision ID: 4c2161973976
Revises: 22c4446398f9
Create Date: 2026-03-11 12:52:31.004943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '4c2161973976'
down_revision: Union[str, Sequence[str], None] = '22c4446398f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('recommendations', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'fk_recommendations_user_id_users',
        'recommendations',
        'users',
        ['user_id'],
        ['id'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_recommendations_user_id_users', 'recommendations', type_='foreignkey')
    op.drop_column('recommendations', 'user_id')

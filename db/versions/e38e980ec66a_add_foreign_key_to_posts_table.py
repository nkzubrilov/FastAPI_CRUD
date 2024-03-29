"""Add foreign key to posts table

Revision ID: e38e980ec66a
Revises: c9beef03aff4
Create Date: 2024-03-28 16:12:32.698982

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e38e980ec66a'
down_revision: Union[str, None] = 'c9beef03aff4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users',
                          local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', 'posts')
    op.drop_column('posts', 'user_id')

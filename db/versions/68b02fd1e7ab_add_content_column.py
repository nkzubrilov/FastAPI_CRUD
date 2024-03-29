"""Add content column

Revision ID: 68b02fd1e7ab
Revises: d0f523d4b3d9
Create Date: 2024-03-28 15:46:14.215428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68b02fd1e7ab'
down_revision: Union[str, None] = 'd0f523d4b3d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')

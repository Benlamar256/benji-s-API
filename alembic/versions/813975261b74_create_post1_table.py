"""(create post1 table)

Revision ID: 813975261b74
Revises: 
Create Date: 2024-03-30 10:51:55.154508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '813975261b74'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('post1', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title',sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('post1')
    pass

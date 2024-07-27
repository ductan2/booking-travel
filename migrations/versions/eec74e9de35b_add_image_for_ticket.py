"""add image for ticket

Revision ID: eec74e9de35b
Revises: e2507dba9c85
Create Date: 2024-07-27 17:34:21.680220

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eec74e9de35b'
down_revision: Union[str, None] = 'e2507dba9c85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickettravel', sa.Column('image', sqlmodel.sql.sqltypes.AutoString(length=2083), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tickettravel', 'image')
    # ### end Alembic commands ###

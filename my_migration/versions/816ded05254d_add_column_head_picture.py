"""add column head_picture

Revision ID: 816ded05254d
Revises: 
Create Date: 2017-11-09 17:06:24.317000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '816ded05254d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('head_picture', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'head_picture')
    # ### end Alembic commands ###

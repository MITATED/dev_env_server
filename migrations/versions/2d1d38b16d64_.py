"""empty message

Revision ID: 2d1d38b16d64
Revises: a65bf6c9a4f9
Create Date: 2018-08-07 15:59:13.247604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d1d38b16d64'
down_revision = 'a65bf6c9a4f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('form', sa.Column('slug', sa.String(length=140), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('form', 'slug')
    # ### end Alembic commands ###

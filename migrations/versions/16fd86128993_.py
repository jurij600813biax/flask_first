"""empty message

Revision ID: 16fd86128993
Revises: ae70ace64a28
Create Date: 2020-04-28 16:30:51.170667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16fd86128993'
down_revision = 'ae70ace64a28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('product_photo', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'product_photo')
    # ### end Alembic commands ###
"""empty message

Revision ID: d1cbeec41ba3
Revises: 95b0082d619f
Create Date: 2020-02-09 20:43:31.089808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1cbeec41ba3'
down_revision = '95b0082d619f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shops', sa.Column('owner', sa.Integer(), nullable=True))
    op.drop_constraint('shops_admin_fkey', 'shops', type_='foreignkey')
    op.create_foreign_key(None, 'shops', 'users', ['owner'], ['id'])
    op.drop_column('shops', 'admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shops', sa.Column('admin', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'shops', type_='foreignkey')
    op.create_foreign_key('shops_admin_fkey', 'shops', 'users', ['admin'], ['id'])
    op.drop_column('shops', 'owner')
    # ### end Alembic commands ###

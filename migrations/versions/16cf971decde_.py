"""empty message

Revision ID: 16cf971decde
Revises: 7ad2e93ef375
Create Date: 2020-02-13 19:56:50.966256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16cf971decde'
down_revision = '7ad2e93ef375'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('icon_delete_hash', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'icon_delete_hash')
    # ### end Alembic commands ###

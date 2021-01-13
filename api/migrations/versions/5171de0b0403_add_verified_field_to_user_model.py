"""add 'verified' field to User model

Revision ID: 5171de0b0403
Revises: 5d988c97b3b7
Create Date: 2021-01-02 22:52:45.718436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5171de0b0403'
down_revision = '5d988c97b3b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('verified', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('verified')

    # ### end Alembic commands ###
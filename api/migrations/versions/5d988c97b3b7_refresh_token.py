"""refresh token

Revision ID: 5d988c97b3b7
Revises: 0c9fc0685667
Create Date: 2020-10-26 05:55:59.036613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d988c97b3b7'
down_revision = '0c9fc0685667'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('refresh_token', sa.String(length=32), nullable=True))
    op.add_column('user', sa.Column('refresh_token_expiration', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_refresh_token'), 'user', ['refresh_token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_refresh_token'), table_name='user')
    op.drop_column('user', 'refresh_token_expiration')
    op.drop_column('user', 'refresh_token')
    # ### end Alembic commands ###
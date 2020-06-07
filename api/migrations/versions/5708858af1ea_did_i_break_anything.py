"""did I break anything?

Revision ID: 5708858af1ea
Revises: b023ea341c31
Create Date: 2020-06-07 05:52:30.574995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5708858af1ea'
down_revision = 'b023ea341c31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('lesson_liked_by_fkey', 'lesson', type_='foreignkey')
    op.drop_column('lesson', 'liked_by')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lesson', sa.Column('liked_by', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('lesson_liked_by_fkey', 'lesson', 'user', ['liked_by'], ['id'])
    # ### end Alembic commands ###

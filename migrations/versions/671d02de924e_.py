"""empty message

Revision ID: 671d02de924e
Revises: 86fc0f8be768
Create Date: 2022-07-01 23:10:13.268029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '671d02de924e'
down_revision = '86fc0f8be768'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=32), nullable=False),
    sa.Column('thought_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['thought_id'], ['thought.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tag')
    # ### end Alembic commands ###

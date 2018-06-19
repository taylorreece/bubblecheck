"""empty message

Revision ID: 2aecebdb8223
Revises: fb46951d763b
Create Date: 2018-06-18 21:13:13.834635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2aecebdb8223'
down_revision = 'fb46951d763b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('colleagues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('modified', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('colleague1', sa.Integer(), nullable=True),
    sa.Column('colleague2', sa.Integer(), nullable=True),
    sa.Column('accepted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['colleague1'], ['users.id'], ),
    sa.ForeignKeyConstraint(['colleague2'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('colleagues')
    # ### end Alembic commands ###
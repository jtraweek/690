"""Testing migrate of initial tables

Revision ID: dbf65982926b
Revises: 
Create Date: 2017-09-18 10:34:12.952071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbf65982926b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trip',
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('about', sa.String(), nullable=True),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.Column('icon', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('trip_id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('_password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('activity',
    sa.Column('activity_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('length', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('trip_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.trip_id'], ),
    sa.PrimaryKeyConstraint('activity_id')
    )
    op.create_table('trip_photo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filepath', sa.String(), nullable=True),
    sa.Column('trip_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.trip_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_trips',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('trip_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.trip_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_trips')
    op.drop_table('trip_photo')
    op.drop_table('activity')
    op.drop_table('user')
    op.drop_table('trip')
    # ### end Alembic commands ###

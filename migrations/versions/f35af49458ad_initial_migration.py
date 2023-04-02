"""Initial migration

Revision ID: f35af49458ad
Revises: 
Create Date: 2023-04-02 22:20:09.625279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f35af49458ad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userdbs')
    op.drop_table('history')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('login', sa.TEXT(), nullable=True),
    sa.Column('password', sa.TEXT(), nullable=True),
    sa.Column('avatar', sa.BLOB(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('history',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('request', sa.TEXT(), nullable=True),
    sa.Column('namedb', sa.TEXT(), nullable=True),
    sa.Column('time', sa.TEXT(), nullable=True),
    sa.Column('condition', sa.TEXT(), nullable=True),
    sa.Column('owner', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['user.login'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userdbs',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('db_info', sa.TEXT(), nullable=True),
    sa.Column('owner', sa.TEXT(), nullable=True),
    sa.Column('dbName', sa.TEXT(), nullable=True),
    sa.Column('vender', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['user.login'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

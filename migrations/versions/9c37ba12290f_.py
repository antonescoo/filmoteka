"""empty message

Revision ID: 9c37ba12290f
Revises: 134ff666d36e
Create Date: 2022-05-20 18:00:27.382459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c37ba12290f'
down_revision = '134ff666d36e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_unique_constraint(None, 'films', ['slug'])
    op.add_column('user', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('user', sa.Column('active', sa.Boolean(), nullable=True))
    op.drop_column('user', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('user', 'active')
    op.drop_column('user', 'id')
    op.drop_constraint(None, 'films', type_='unique')
    op.drop_table('roles_users')
    op.drop_table('role')
    # ### end Alembic commands ###

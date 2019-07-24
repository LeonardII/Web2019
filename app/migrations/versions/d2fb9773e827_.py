"""empty message

Revision ID: d2fb9773e827
Revises: 3b41186b48f4
Create Date: 2019-07-18 18:30:01.618057

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd2fb9773e827'
down_revision = '3b41186b48f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.String(length=80), nullable=False))
    op.drop_column('user', 'Passwort')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('Passwort', mysql.VARCHAR(collation='utf8_unicode_ci', length=80), nullable=False))
    op.drop_column('user', 'password_hash')
    # ### end Alembic commands ###
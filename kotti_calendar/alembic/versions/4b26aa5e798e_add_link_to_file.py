"""Add link_to_file

Revision ID: 4b26aa5e798e
Revises: 1c3e72660e31
Create Date: 2013-03-01 23:02:21.817168

"""

# revision identifiers, used by Alembic.
revision = '4b26aa5e798e'
down_revision = '1c3e72660e31'

from alembic import op
import sqlalchemy as sa


def upgrade():

    op.add_column("events", sa.Column("link_to_file", sa.Boolean(create_constraint=False)))


def downgrade():

    op.drop_column("events", "link_to_file")

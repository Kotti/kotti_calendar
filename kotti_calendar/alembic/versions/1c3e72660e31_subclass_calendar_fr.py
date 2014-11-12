"""Subclass Calendar from Document

Revision ID: 1c3e72660e31
Revises: 1617f961c382
Create Date: 2013-03-01 21:23:57.549839

"""

# revision identifiers, used by Alembic.
revision = '1c3e72660e31'
down_revision = '1617f961c382'

from alembic import op
from kotti.sqla import JsonType
import sqlalchemy as sa


def upgrade():

    op.execute('ALTER TABLE calendars RENAME TO old_calendars')

    op.create_table(
        'calendars',
        sa.Column(
            'id',
            sa.Integer(),
            sa.ForeignKey('documents.id'),
            primary_key=True
            ),
        sa.Column(
            'feeds',
            JsonType(),
            nullable=False
            ),
        sa.Column(
            'weekends',
            sa.Boolean()
            )
        )

    op.execute('INSERT INTO calendars SELECT * FROM old_calendars')
    op.execute('INSERT INTO documents (id) SELECT id FROM old_calendars')
    op.drop_table('old_calendars')


def downgrade():

    op.execute('ALTER TABLE calendars RENAME TO old_calendars')

    op.create_table(
        'calendars',
        sa.Column(
            'id',
            sa.Integer(),
            sa.ForeignKey('contents.id'),
            primary_key=True
            ),
        sa.Column(
            'feeds',
            JsonType(),
            nullable=False
            ),
        sa.Column(
            'weekends',
            sa.Boolean()
            )
        )

    op.execute('INSERT INTO calendars SELECT * FROM old_calendars')
    op.execute('DELETE FROM documents WHERE id in (SELECT id FROM old_calendars)')
    op.drop_table('old_calendars')

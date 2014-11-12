"""Subclass Event from Document

Revision ID: 1617f961c382
Revises: None
Create Date: 2013-03-01 22:32:06.259214

"""

# revision identifiers, used by Alembic.
revision = '1617f961c382'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():

    op.execute('ALTER TABLE events RENAME TO old_events')

    op.create_table(
        'events',
        sa.Column(
            'id',
            sa.Integer(),
            sa.ForeignKey('documents.id'),
            primary_key=True
            ),
        sa.Column(
            'start',
            sa.DateTime(),
            nullable=False
            ),
        sa.Column(
            'end',
            sa.DateTime()
            ),
        sa.Column(
            'all_day',
            sa.Boolean()
            )
        )

    op.execute('INSERT INTO events SELECT * FROM old_events')
    op.execute('INSERT INTO documents (id) SELECT id FROM old_events')
    op.drop_table('old_events')


def downgrade():

    op.execute('ALTER TABLE events RENAME TO old_events')

    op.create_table(
        'events',
        sa.Column(
            'id',
            sa.Integer(),
            sa.ForeignKey('contents.id'),
            primary_key=True
            ),
        sa.Column(
            'start',
            sa.DateTime(),
            nullable=False
            ),
        sa.Column(
            'end',
            sa.DateTime()
            ),
        sa.Column(
            'all_day',
            sa.Boolean()
            )
        )

    op.execute('INSERT INTO events SELECT * FROM old_events')
    op.execute('DELETE FROM documents WHERE id in (SELECT id FROM old_events)')
    op.drop_table('old_events')

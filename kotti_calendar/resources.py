from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.orm import mapper
from kotti import metadata
from kotti.resources import Content
from kotti.util import JsonType

class Calendar(Content):
    type_info = Content.type_info.copy(
        name=u'Calendar',
        add_view=u'add_calendar',
        addable_to=[u'Document'],
        )

    def __init__(self, feeds=(), weekends=True, **kwargs):
        super(Calendar, self).__init__(**kwargs)
        self.feeds = feeds
        self.weekends = weekends

class Event(Content):
    type_info = Content.type_info.copy(
        name=u'Event',
        add_view=u'add_event',
        addable_to=[u'Calendar'],
        )

    def __init__(self, start=None, end=None, all_day=False,
                 in_navigation=False, **kwargs):
        super(Event, self).__init__(in_navigation=in_navigation, **kwargs)
        self.start = start
        self.end = end
        self.all_day = all_day


calendars = Table('calendars', metadata,
    Column('id', Integer, ForeignKey('contents.id'), primary_key=True),
    Column('feeds', JsonType(), nullable=False),
    Column('weekends', Boolean()),
)

events = Table('events', metadata,
    Column('id', Integer, ForeignKey('contents.id'), primary_key=True),
    Column('start', DateTime(), nullable=False),
    Column('end', DateTime()),
    Column('all_day', Boolean()),
)

mapper(Calendar, calendars, inherits=Content, polymorphic_identity='calendar')
mapper(Event, events, inherits=Content, polymorphic_identity='event')

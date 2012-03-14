from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from kotti.resources import Content
from kotti.util import JsonType

class Calendar(Content):
    id = Column(Integer, ForeignKey('contents.id'), primary_key=True)
    feeds = Column(JsonType(), nullable=False)
    weekends = Column(Boolean())

    type_info = Content.type_info.copy(
        name=u'Calendar',
        title=u'Calendar',
        add_view=u'add_calendar',
        addable_to=[u'Document'],
        )

    def __init__(self, feeds=(), weekends=True, **kwargs):
        super(Calendar, self).__init__(**kwargs)
        self.feeds = feeds
        self.weekends = weekends

class Event(Content):
    id = Column('id', Integer, ForeignKey('contents.id'), primary_key=True)
    start = Column('start', DateTime(), nullable=False)
    end = Column('end', DateTime())
    all_day = Column('all_day', Boolean())

    type_info = Content.type_info.copy(
        name=u'Event',
        title=u'Event',
        add_view=u'add_event',
        addable_to=[u'Calendar'],
        )

    def __init__(self, start=None, end=None, all_day=False,
                 in_navigation=False, **kwargs):
        super(Event, self).__init__(in_navigation=in_navigation, **kwargs)
        self.start = start
        self.end = end
        self.all_day = all_day

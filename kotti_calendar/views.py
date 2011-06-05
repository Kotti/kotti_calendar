import datetime
from pyramid.compat import json
from pyramid.url import resource_url

import colander
from sqlalchemy import desc
from kotti import DBSession
from kotti.views.edit import ContentSchema
from kotti.views.edit import generic_edit
from kotti.views.edit import generic_add
from kotti.views.view import view_node
from kotti.views.util import ensure_view_selector
from kotti.views.util import template_api

from kotti_calendar.resources import Calendar
from kotti_calendar.resources import Event

class Feeds(colander.SequenceSchema):
    feed = colander.SchemaNode(
        colander.String(),
        missing=None,
        )

class CalendarSchema(ContentSchema):
    feeds = Feeds(
        missing=[],
        title=u"Calendar feeds",
        description=u"Paste Google calendar XML feeds here",
        )
    weekends = colander.SchemaNode(colander.Boolean())

class EventSchema(ContentSchema):
    start = colander.SchemaNode(
        colander.DateTime(default_tzinfo=None))
    end = colander.SchemaNode(
        colander.DateTime(default_tzinfo=None), missing=None)
    all_day = colander.SchemaNode(colander.Boolean())

@ensure_view_selector
def edit_calendar(context, request):
    return generic_edit(context, request, CalendarSchema())

def add_calendar(context, request):
    return generic_add(context, request, CalendarSchema(), Calendar, u'calendar')

@ensure_view_selector
def edit_event(context, request):
    return generic_edit(context, request, EventSchema())

def add_event(context, request):
    return generic_add(context, request, EventSchema(), Event, u'event')

def view_calendar(context, request):
    session = DBSession()
    now = datetime.datetime.now()
    query = session.query(Event).filter(Event.parent_id==context.id)
    upcoming = query.filter(Event.start > now).order_by(Event.start).all()
    past = query.filter(Event.start < now).order_by(desc(Event.start)).all()

    fmt = '%Y-%m-%d %H:%M:%S'
    fullcalendar_events = []
    for event in (upcoming + past):
        json_event = {
            'title': event.title,
            'url': resource_url(event, request),
            'start': event.start.strftime(fmt),
            'allDay': event.all_day,
            }
        if event.end:
            json_event['end'] = event.end.strftime(fmt)
        fullcalendar_events.append(json_event)

    fullcalendar_options = {
        'eventSources': context.feeds,
        'weekends': context.weekends,
        'events': fullcalendar_events,
        }

    return {
        'api': template_api(context, request),
        'upcoming_events': upcoming,
        'past_events': past,
        'fullcalendar_options': json.dumps(fullcalendar_options),
        }

def includeme_edit(config):
    config.add_view(
        edit_calendar,
        context=Calendar,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        add_calendar,
        name=Calendar.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        edit_event,
        context=Event,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        add_event,
        name=Event.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )

def includeme_view(config):
    config.add_view(
        view_calendar,
        context=Calendar,
        name='view',
        permission='view',
        renderer='templates/calendar-view.pt',
        )

    config.add_view(
        view_node,
        context=Event,
        name='view',
        permission='view',
        renderer='templates/event-view.pt',
        )

    config.add_static_view('static-kotti_calendar', 'kotti_calendar:static')

def includeme(config):
    includeme_edit(config)
    includeme_view(config)

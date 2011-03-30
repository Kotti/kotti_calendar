import datetime

import colander
from sqlalchemy import desc
from kotti import DBSession
from kotti.views.edit import NodeSchema
from kotti.views.edit import generic_edit
from kotti.views.edit import generic_add
from kotti.views.view import view_node
from kotti.views.util import ensure_view_selector
from kotti.views.util import TemplateAPI

from kotti_calendar.resources import Calendar
from kotti_calendar.resources import Event

class EventSchema(NodeSchema):
    start = colander.SchemaNode(
        colander.DateTime(default_tzinfo=None))
    end = colander.SchemaNode(
        colander.DateTime(default_tzinfo=None), missing=None)
    all_day = colander.SchemaNode(colander.Boolean())

@ensure_view_selector
def edit_calendar(context, request):
    return generic_edit(context, request, NodeSchema())

def add_calendar(context, request):
    return generic_add(context, request, NodeSchema(), Calendar, u'calendar')

@ensure_view_selector
def edit_event(context, request):
    return generic_edit(context, request, EventSchema())

def add_event(context, request):
    return generic_add(context, request, EventSchema(), Event, u'event')

def view_calendar(context, request):
    session = DBSession()
    now = datetime.datetime.now()
    query = session.query(Event).filter(Event.parent_id==context.id)
    upcoming = query.filter(Event.start > now).order_by(Event.start)
    past = query.filter(Event.start < now).order_by(desc(Event.start))
    return {
        'api': TemplateAPI(context, request),
        'upcoming_events': upcoming,
        'past_events': past,
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

def includeme(config):
    includeme_edit(config)
    includeme_view(config)


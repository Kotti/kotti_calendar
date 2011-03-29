import colander
from kotti.views.edit import NodeSchema
from kotti.views.edit import generic_edit
from kotti.views.edit import generic_add
from kotti.views.util import ensure_view_selector

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
    return generic_add(context, request, NodeSchema(), Calendar)

@ensure_view_selector
def edit_event(context, request):
    return generic_edit(context, request, EventSchema())

def add_event(context, request):
    return generic_add(context, request, EventSchema(), Event)

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

def includeme(config):
    includeme_edit(config)

import datetime
from kotti import DBSession
from kotti.views.slots import assign_slot
from kotti_calendar.resources import Event


def upcoming_events(context, request):
    now = datetime.datetime.now()
    events = DBSession.query(Event).filter(Event.start > now)\
                .order_by(Event.start).all()
    return {'events': events}


def includeme_upcoming_events(config):
    config.add_view(
        upcoming_events,
        name='upcoming-events',
        renderer='kotti_calendar:templates/upcoming-events.pt')
    assign_slot('upcoming-events', 'right')

from datetime import datetime
from datetime import timedelta

import transaction
from kotti.testing import DummyRequest
from pyramid.threadlocal import get_current_registry
from pytest import mark


@mark.user('admin')
def test_render(webtest, root):

    from kotti_calendar.resources import Calendar
    from kotti_calendar.resources import Event

    root['calendar'] = calendar = Calendar(title=u'Calendar')
    calendar['event'] = Event(
        title=u'This is my Event',
        start=datetime(2112, 8, 22, 20, 0, 0),
        end=datetime(2112, 8, 22, 22, 0, 0),
        )

    resp = webtest.get('/')
    assert 'This is my Event' in resp.body
    assert 'Aug 22, 2112 8:00:00 PM' in resp.body


def test_view(root, workflow):

    from kotti.workflow import get_workflow
    from kotti_calendar.resources import Calendar
    from kotti_calendar.resources import Event
    from kotti_calendar.widgets import upcoming_events

    now = datetime.now()

    result = upcoming_events(root, DummyRequest())
    assert len(result['events']) == 0

    root['calendar'] = Calendar()
    root['calendar']['event1'] = event1 = Event(
        title=u'Event 1',
        start=now - timedelta(1),
        end=now + timedelta(2))
    root['calendar']['event2'] = event2 = Event(
        title=u'Event 2',
        start=now + timedelta(1),
        end=now + timedelta(2))

    wf = get_workflow(event1)
    wf.transition_to_state(event1, None, u'public')
    wf = get_workflow(event2)
    wf.transition_to_state(event2, None, u'public')

    result = upcoming_events(root, DummyRequest())

    events = result['events']
    assert len(events) == 2
    assert events[0].title == u'Event 1'
    assert events[0].start == now - timedelta(1)
    assert events[1].title == u'Event 2'
    assert events[1].start == now + timedelta(1)


@mark.user('admin')
def test_settings(webtest, root):

    from kotti_calendar.resources import Calendar
    from kotti_calendar.resources import Event

    root['calendar'] = calendar = Calendar(title=u'Calendar')

    for c in range(6):
        calendar['event-%d' % c] = Event(
            title=u'Event %d' % c,
            start=datetime(2112, 8, 23, c, 0, 0))

    transaction.commit()

    resp = webtest.get('/')
    assert u"Event 5" not in resp.body

    settings = get_current_registry().settings
    settings['kotti_calendar.upcoming_events_widget.events_count'] = u'nan'
    resp = webtest.get('/')
    assert u"Event 5" not in resp.body

    settings = get_current_registry().settings
    settings['kotti_calendar.upcoming_events_widget.events_count'] = u'7'
    resp = webtest.get('/')
    assert u"Event 5" in resp.body

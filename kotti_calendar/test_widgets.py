from datetime import (
    datetime,
    timedelta,
)
from kotti.testing import (
    FunctionalTestBase,
    DummyRequest,
)


class TestUpcomingEventsWidget(FunctionalTestBase):

    def setUp(self):
        conf = {'kotti.configurators': 'kotti_calendar.kotti_configure',
                'pyramid.includes': 'kotti_calendar.widgets.includeme_upcoming_events',
                }
        super(TestUpcomingEventsWidget, self).setUp(**conf)

    def test_view(self):
        from kotti_calendar.widgets import upcoming_events
        from kotti.resources import get_root
        from kotti_calendar.resources import Calendar
        from kotti_calendar.resources import Event

        now = datetime.now()
        root = get_root()

        result = upcoming_events(root, DummyRequest())
        assert len(result['events']) == 0

        root['calendar'] = Calendar()
        root['calendar']['event1'] = Event(title=u'Event 1',
                                           start=now + timedelta(1),
                                           end=now + timedelta(2))
        root['calendar']['event2'] = Event(title=u'Event 2',
                                           start=now + timedelta(1),
                                           end=now + timedelta(2))
        result = upcoming_events(root, DummyRequest())
        assert len(result['events']) == 2
        assert result['events'][0].title == u'Event 1'
        assert result['events'][0].start == now + timedelta(1)

    def test_render(self):
        browser = self.login_testbrowser()
        ctrl = browser.getControl

        browser.getLink(u'Calendar').click()
        ctrl('Title').value = u'Calendar'
        ctrl(name=u'save').click()

        browser.getLink(u'Event').click()
        ctrl('Title').value = u'This is my Event'
        ctrl('Start').value = u'2112-08-22 20:00:00'
        ctrl('End').value = u'2112-08-22 22:00:00'
        ctrl(name=u'save').click()

        browser.open(self.BASE_URL)
        assert 'This is my Event' in browser.contents
        assert 'Aug 22, 2112 8:00:00 PM' in browser.contents

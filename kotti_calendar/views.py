# -*- coding: utf-8 -*-

import colander
import datetime
from js.fullcalendar import lang_all_js
from kotti.resources import File
from kotti.security import has_permission
from kotti.views.edit import DocumentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from kotti.views.util import template_api
from pyramid.compat import json
from pyramid.i18n import get_locale_name
from pyramid.url import resource_url
from pyramid.view import view_config
from pyramid.view import view_defaults
from sqlalchemy import desc
from sqlalchemy.sql.expression import or_

from kotti_calendar import _
from kotti_calendar.resources import Calendar
from kotti_calendar.resources import Event
from kotti_calendar.fanstatic import kotti_calendar_resources


class Feeds(colander.SequenceSchema):
    """ Schema for calendar feeds. """

    feed = colander.SchemaNode(
        colander.String(),
        title=_(u"Feed"),
        missing=None,
        )


class CalendarSchema(DocumentSchema):
    """ Schema for calendars. """

    feeds = Feeds(
        missing=[],
        title=_(u"Calendar feeds"),
        description=_(u"Paste Google calendar XML feeds here"),
        )
    weekends = colander.SchemaNode(
        colander.Boolean(),
        title=_(u"Weekends"))


class EventSchema(DocumentSchema):
    """ Schema for events. """

    start = colander.SchemaNode(
        colander.DateTime(default_tzinfo=None),
        title=_(u"Start"))
    end = colander.SchemaNode(
        colander.DateTime(default_tzinfo=None),
        title=_(u"End"),
        missing=None)
    all_day = colander.SchemaNode(
        colander.Boolean(),
        title=_(u"All day"))
    link_to_file = colander.SchemaNode(
        colander.Boolean(),
        title=_(u"Link to File"),
        description=_(u"When activated, the link in an associated calendar "
                      u"view points to the first contained file of the event "
                      u"(instead of to the calendar node)."))


@view_config(name=Calendar.type_info.add_view, permission='add',
             renderer='kotti:templates/edit/node.pt')
class CalendarAddForm(AddFormView):
    """ Form to add a new calendar. """

    schema_factory = CalendarSchema
    add = Calendar
    item_type = _(u"Calendar")


@view_config(name='edit', context=Calendar, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class CalendarEditForm(EditFormView):
    """ Form to edit existing calendars. """

    schema_factory = CalendarSchema


@view_config(name=Event.type_info.add_view, permission='add',
             renderer='kotti:templates/edit/node.pt')
class EventAddForm(AddFormView):
    """ Form to add a new event. """

    schema_factory = EventSchema
    add = Event
    item_type = _(u"Event")


@view_config(name='edit', context=Event, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class EventEditForm(EditFormView):
    """ Form to edit existing events. """

    schema_factory = EventSchema


class BaseView(object):
    """ Simple base view. """

    def __init__(self, context, request):
        """ Constructor.

        :param context: Current context.
        :type context: :class:`kotti.resources.Content` or subclass.

        :param request: Current request.
        :type request: :class:`pyramid.request.Request`
        """

        self.context = context
        self.request = request


@view_defaults(context=Calendar, permission='view')
class CalendarViews(BaseView):
    """ Views for calendars. """

    def event_url(self, event):
        """ Return the URL for an event in the calendar view.

        :param event: Event for which the URL is requested.
        :type event: :class:`kotti_calendar.resources.Event`

        :result: URL
        :rtype: str
        """

        url = resource_url(event, self.request)

        if event.link_to_file:
            files = File.query.filter(File.parent_id == event.id)\
                .order_by(File.position).all()
            for f in files:
                if has_permission('view', f, self.request):
                    url = resource_url(f, self.request, '@@attachment-view')
                    break
        return url

    @property
    def past_events(self):
        """ List events in the past.

        :result: List of events.
        :rtype: list of :class:`kotti_calendar.resources.Event`
        """

        now = datetime.datetime.now()

        events = Event.query \
            .filter(Event.parent_id == self.context.id) \
            .filter(Event.start < now)\
            .order_by(desc(Event.start))\
            .all()

        return [event for event in events
                if has_permission('view', event, self.request)]

    @property
    def upcoming_events(self):
        """ List events in the future.

        :result: List of events.
        :rtype: list of :class:`kotti_calendar.resources.Event`
        """

        now = datetime.datetime.now()

        events = Event.query \
            .filter(Event.parent_id == self.context.id) \
            .filter(or_(Event.start > now, Event.end > now))\
            .order_by(Event.start)\
            .all()

        return [event for event in events
                if has_permission('view', event, self.request)]

    @property
    def fullcalendar_events(self):
        """ Events to display in FullCalendar widget.

        :result: JSON serializable list of events.
        :rtype: list of dict
        """

        fmt = '%Y-%m-%d %H:%M:%S'
        events = []

        for event in (self.upcoming_events + self.past_events):

            json_event = {
                'title': event.title,
                'url': self.event_url(event),
                'start': event.start.strftime(fmt),
                'allDay': event.all_day,
                }
            if event.end:
                json_event['end'] = event.end.strftime(fmt)
            events.append(json_event)

        return events

    @property
    def fullcalendar_options(self):
        """ Options object suitable for FullCalendar initialization.

        :result: JSON serializable FullCalendar options.
        :rtype: dict
        """

        lang = get_locale_name(self.request) or 'en'

        return {
            'header': {
                'left': 'prev,next today',
                'center': 'title',
                'right': 'month,agendaWeek,agendaDay'
            },
            'eventSources': self.context.feeds,
            'weekends': self.context.weekends,
            'events': self.fullcalendar_events,
            'lang': lang,
        }

    @view_config(name='view', renderer='templates/calendar-view.pt')
    def view(self):
        """ Default view for :class:`kotti_calendar.resources.Calendar`

        :result: Dictionary needed to render the template.
        :rtype: dict
        """

        kotti_calendar_resources.need()
        lang_all_js.need()

        return {
            'api': template_api(self.context, self.request),
            'upcoming_events': self.upcoming_events,
            'past_events': self.past_events,
            'fullcalendar_options': json.dumps(self.fullcalendar_options),
            'event_url': self.event_url,
            }


@view_defaults(context=Event, permission='view')
class EventViews(BaseView):
    """ Views for events. """

    @property
    def files(self):
        """ Files that the event contains.
        :result: List of files.
        :rtype: list of :class:`kotti.resources.File`
        """

        files = File.query.filter(File.parent_id == self.context.id)\
            .order_by(File.position).all()

        return [f for f in files if has_permission('view', f, self.request)]

    @view_config(name='view', renderer='templates/event-view.pt')
    def view(self):
        """ Default view for :class:`kotti_calendar.resources.Event`

        :result: Dictionary needed to render the template.
        :rtype: dict
        """

        return {
            'files': self.files,
        }

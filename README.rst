==============
kotti_calendar
==============

This is an extension to the Kotti CMS that allows you to add calendars
with events to your Kotti site.

It uses the `FullCalendar jQuery plugin`_ to display calendars.

Events can be either pulled from Google calendar XML feeds or added in
Kotti itself.

`Find out more about Kotti`_

Setup
=====

To activate the kotti_calendar add-on in your Kotti site, you need to
add an entry to the ``kotti.configurators`` setting in your Paste
Deploy config.  If you don't have a ``kotti.configurators`` option,
add one.  The line in your ``[app:main]`` section could then look
like this::

  kotti.configurators = kotti_calendar.kotti_configure

With this, you'll be able to add calendar and event items in your site.


Upcoming events widget
----------------------

kotti_calendar provides a upcoming events widget, which is disabled by default.
To enable the widget add the following to the ``pyramid.includes`` setting::

  pyramid.includes = kotti_calendar.widgets.includeme_upcoming_events

With this, the upcoming events will be shown in the right column of the site.

You can adjust how many events will be shown in the widget with set
``kotti_calendar.upcoming_events_widget.events_count`` to a different
value. It defaults to ``5``::

    kotti_calendar.upcoming_events_widget.events_count = 10

.. _FullCalendar jQuery plugin: http://arshaw.com/fullcalendar/
.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti

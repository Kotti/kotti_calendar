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
add one.  The line in your ``[app:Kotti]`` section could then look
like this::

  kotti.configurators = kotti_calendar.kotti_configure

With this, you'll be able to add calendar and event items in your site.


.. _FullCalendar jQuery plugin: http://arshaw.com/fullcalendar/
.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti

# -*- coding: utf-8 -*-

from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from js.fullcalendar import fullcalendar_css
from js.fullcalendar import fullcalendar_print_css
from js.fullcalendar import fullcalendar_js
from js.fullcalendar import gcal_js


library = Library("kotti_calendar", "static")

kotti_calendar_css = Resource(
    library,
    "style.css",
    minified="style.min.css")

css = Group([fullcalendar_css, fullcalendar_print_css, kotti_calendar_css])
js = Group([fullcalendar_js, gcal_js])

kotti_calendar_resources = Group([css, js])

# -*- coding: utf-8 -*-

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from js.jquery import jquery


lib = Library("kotti_calendar", "static")

fullcalendar_css = Resource(
    lib,
    "fullcalendar/fullcalendar.css",
    minified="fullcalendar/fullcalendar.min.css")

fullcalendar_print_css = Resource(
    lib,
    "fullcalendar/fullcalendar.print.css",
    depends=[fullcalendar_css, ],
    minified="fullcalendar/fullcalendar.print.min.css")

fullcalendar_js = Resource(
    lib,
    "fullcalendar/fullcalendar.js",
    depends=[jquery, ],
    minified="fullcalendar/fullcalendar.min.js")

gcal_js = Resource(
    lib,
    "fullcalendar/gcal.js",
    depends=[fullcalendar_js, ],
    minified="fullcalendar/gcal.min.js")

fullcalendar_locales = {
    "de": Resource(
        lib,
        "fullcalendar/fullcalendar_de.js",
        depends=[fullcalendar_js, ],
        minified="fullcalendar/fullcalendar_de.min.js"),
    "en": Resource(
        lib,
        "fullcalendar/fullcalendar_en.js",
        depends=[fullcalendar_js, ],
        minified="fullcalendar/fullcalendar_en.min.js"),
}

kotti_calendar_css = Resource(
    lib,
    "style.css",
    minified="style.min.css")

css = Group([fullcalendar_css, fullcalendar_print_css, kotti_calendar_css])
js = Group([fullcalendar_js, gcal_js])

kotti_calendar_resources = Group([css, js])

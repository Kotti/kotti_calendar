# -*- coding: utf-8 -*-

from kotti.resources import File
from kotti.util import extract_from_settings
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_calendar')


def events_settings(name=''):

    prefix = 'kotti_calendar.upcoming_events_widget.'
    if name:
        prefix += name + '.'  # pragma: no cover
    settings = EVENTS_WIDGET_DEFAULTS.copy()
    settings.update(extract_from_settings(prefix))
    try:
        settings['events_count'] = int(settings['events_count'])
    except ValueError:
        settings['events_count'] = 5
    return settings


EVENTS_WIDGET_DEFAULTS = {
    'events_count': '5',
    }


def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_calendar.kotti_configure

        to enable the ``kotti_calendar`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings['pyramid.includes'] += ' kotti_calendar'
    settings['kotti.available_types'] += ' kotti_calendar.resources.Calendar kotti_calendar.resources.Event'
    File.type_info.addable_to.append('Event')


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, add the ``kotti_configure``
        above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_translation_dirs('kotti_calendar:locale')
    config.add_static_view('static-kotti_calendar', 'kotti_calendar:static')

    config.scan(__name__)

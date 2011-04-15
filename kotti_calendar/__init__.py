def kotti_configure(settings):
    settings['kotti.includes'] += ' kotti_calendar.views'
    settings['kotti.available_types'] += ' kotti_calendar.resources.Calendar kotti_calendar.resources.Event'

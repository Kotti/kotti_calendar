def kotti_configure(config):
    config['kotti.includes'] += ' kotti_calendar.views'
    config['kotti.available_types'] += ' kotti_calendar.resources.Calendar kotti_calendar.resources.Event'

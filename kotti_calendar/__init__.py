def kotti_configure(settings):
    settings['kotti.includes'] += ' kotti_calendar.views'
    settings['kotti.available_types'] += ' kotti_calendar.resources.Calendar kotti_calendar.resources.Event'


def _patch_colander():
    # https://github.com/dnouri/colander/commit/6a09583a8b9bcae29d6f51ce05434becff379134
    from colander import null
    from colander import DateTime

    save_datetime_serialize = DateTime.serialize

    def datetime_serialize(self, node, appstruct):
        if not appstruct:
            return null
        return save_datetime_serialize(self, node, appstruct)

    DateTime.serialize = datetime_serialize

_patch_colander()

pytest_plugins = "kotti"

import kotti.tests
from kotti.workflow import reset_workflow
from pytest import fixture


@fixture(scope='session')
def settings():
    from kotti import _resolve_dotted
    from kotti import conf_defaults
    from kotti_calendar import kotti_configure

    settings = conf_defaults.copy()
    settings.update({
        'pyramid.includes':
        'kotti_calendar.widgets.includeme_upcoming_events'})
    kotti_configure(settings)
    settings.update({
        'kotti.secret': 'secret',
        'kotti.secret2': 'secret',
        })
    _resolve_dotted(settings)
    return settings


@fixture
def setup_app(settings):
    wsgi_app = kotti.tests.setup_app(settings)
    # The content fixture that calls 'populate' doesn't have events
    # set up.  That's why we need to trigger workflow initialization
    # by hand:
    reset_workflow()
    return wsgi_app


@fixture
def app(db_session, dummy_mailer, events, setup_app):
    return setup_app


@fixture
def webtest(app, monkeypatch, request):
    from webtest import TestApp
    if 'user' in request.keywords:
        login = request.keywords['user'].args[0]
        monkeypatch.setattr(
            "pyramid.authentication."
            "AuthTktAuthenticationPolicy.unauthenticated_userid",
            lambda self, req: login)
    return TestApp(app)

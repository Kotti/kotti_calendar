import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

install_requires = [
    'js.fullcalendar>=2.2.5',
    'Kotti>=0.10b1',
]

tests_require = [
    'pytest-cov',
    'pytest',
    'webtest',
    'wsgi_intercept',
    'zope.testbrowser',
    'Webtest',
]

setup(
    name='kotti_calendar',
    version='0.8.2',
    description="Add a calendar to your Kotti site",
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: Repoze Public License",
        ],
    author='Daniel Nouri',
    author_email='daniel.nouri@gmail.com',
    url='http://pypi.python.org/pypi/kotti_calendar',
    keywords='calendar fullcalendar kotti cms pylons pyramid',
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires + tests_require,
    message_extractors={
        '.': [
            ('**.py', 'lingua_python', None),
            ('**.pt', 'lingua_xml', None),
        ]
    },
    entry_points={
        'fanstatic.libraries': [
            'kotti_calendar = kotti_calendar.fanstatic:library',
        ],
    },
)

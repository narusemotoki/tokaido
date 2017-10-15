#!/usr/bin/env python3
import os

import setuptools


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'SQLAlchemy',
    'colander',
    'pyramid',
    'pyramid_jinja2',
    'pyramid_tm',
    'uwsgi',
    'zope.sqlalchemy',
]

tests_require = [
    'WebTest >= 1.3.1',
    'flake8',
    'mypy',
    'pytest',
    'pytest-cov',
]

setuptools.setup(
    name='tokaido',
    version='0.0.1',
    description="",
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'test': tests_require,
    },
    install_requires=requires,
    entry_points="""\
    [paste.app_factory]
    main = tokaido:main
    """,
)

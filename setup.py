#!/usr/bin/env python

import os
import re
import sys

from setuptools import setup


DIRNAME = os.path.abspath(os.path.dirname(__file__))
rel = lambda *parts: os.path.abspath(os.path.join(DIRNAME, *parts))

with open(rel('README.rst')) as handler:
    README = handler.read()
with open(rel('flask_redis.py')) as handler:
    INIT_PY = handler.read()

INSTALL_REQUIRES = {
    2: ['Flask>=0.8', 'redis>=2.4.11'],
    3: ['Flask>=0.10.1', 'redis>=2.6.2'],
}
VERSION = re.findall("__version__ = '([^']+)'", INIT_PY)[0]


setup(
    name='Flask-And-Redis',
    version=VERSION,
    description='Simple as dead support of Redis database for Flask apps.',
    long_description=README,
    author='Igor Davydenko',
    author_email='playpauseandstop@gmail.com',
    url='https://github.com/playpauseandstop/Flask-And-Redis',
    install_requires=INSTALL_REQUIRES[sys.version_info[0]],
    py_modules=['flask_redis'],
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
    ],
    keywords='flask redis',
    license='BSD License',
)

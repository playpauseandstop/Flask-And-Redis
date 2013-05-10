#!/usr/bin/env python

import os
import re

from distutils.core import setup


DIRNAME = os.path.abspath(os.path.dirname(__file__))
rel = lambda *parts: os.path.abspath(os.path.join(DIRNAME, *parts))

README = open(rel('README.rst')).read()
INIT_PY = open(rel('flask_redis.py')).read()
VERSION = re.findall("__version__ = '([^']+)'", INIT_PY)[0]


setup(
    name='Flask-And-Redis',
    version=VERSION,
    description='Simple as dead support of Redis database for Flask apps.',
    long_description=README,
    author='Igor Davydenko',
    author_email='playpauseandstop@gmail.com',
    url='https://github.com/playpauseandstop/Flask-And-Redis',
    install_requires=[
        'Flask',
        'redis',
    ],
    py_modules=[
        'flask_redis',
    ],
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
    ],
    keywords='flask redis',
    license='BSD License',
)

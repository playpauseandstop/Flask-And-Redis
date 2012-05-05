#!/usr/bin/env python

from setuptools import setup

setup(
    name='Flask-And-Redis',
    version='0.2.1',
    description='Simple as dead support of Redis database for Flask apps.',
    long_description=README,
    author='Lexo Charles',
    author_email='lexo.charles@gmail.com',
    url='https://github.com/sixpoint/Flask-And-Redis',
    install_requires=[
        'setuptools',
        'Flask',
    ],
    packages=[
        'flaskext',
        'flaskext.redis',
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

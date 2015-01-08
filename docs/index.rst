===============
Flask-And-Redis
===============

Flask-And-Redis provides simple as dead support of `Redis <http://redis.io>`_
database for `Flask <http://flask.pocoo.org/>`_ applications. Extension built
around beautiful `redis-py <https://github.com/andymccurdy/redis-py>`_ library
by Andy McCurdy.

* Works on Python 2.6, 2.7, 3.3+
* BSD licensed
* Latest documentation `on Read the Docs
  <http://flask-and-redis.readthedocs.org>`_
* Source, issues and pull requests `on GitHub
  <https://github.com/playpauseandstop/Flask-And-Redis>`_

.. note:: ``Flask-And-Redis`` named as is, cause ``Flask-Redis`` name already
   `taken <http://pypi.python.org/pypi/Flask-Redis>`_, but that library didn't
   match my needs.

Installation
============

Use `pip <http://pip.pypa.org>`_ to install Flask-And-Redis to your system or
virtual environment::

    $ pip install Flask-And-Redis

Otherwise you could download source dist from GitHub or PyPI and put
``flask_redis.py`` file somewhere to ``$PYTHONPATH``, but this way is not
recommended. Use pip for all good things.

Usage
=====

In regular case all you need is importing :class:`~.Redis` instance and
initialize it with ``app`` instance, like::

    from flask import Flask
    from flask_redis import Redis

    app = Flask(__name__)
    redis = Redis(app)

But if you use application factories you could use :meth:`~.Redis.init_app`
method,

::

    redis = Redis()
    # The later on
    app = create_app('config.cfg')
    redis.init_app(app)

Also later you can get ``redis`` connection from ``app.extensions['redis']``
dict, where ``key`` is config prefix and ``value`` is configured redis
connection.

Configuration
=============

``Flask-And-Redis`` understands all keyword arguments which should be passed
to ``redis.StrictRedis`` or ``redis.Redis`` classes init method. In easiest way
all you need is putting

* ``REDIS_HOST``
* ``REDIS_PORT``
* ``REDIS_DB``

to your settings module. Other available settings are:

* ``REDIS_PASSWORD``
* ``REDIS_SOCKET_TIMEOUT``
* ``REDIS_CONNECTION_POOL``
* ``REDIS_CHARSET``
* ``REDIS_ERRORS``
* ``REDIS_DECODE_RESPONSES``
* ``REDIS_UNIX_SOCKET_PATH``

Later these values would initialize redis connection and all public methods of
connection's instance would be copied to :class:`~.Redis`. Also connection
would be stored in ``Redis.connection`` attribute and
``app.extensions['redis']`` dict.

In addition extension has two more configuration options and ability to connect
to multiple redis databases.

REDIS_CLASS
-----------

.. versionadded:: 0.5

Before 0.5 version only ``redis.Redis`` connection used. But as times change
and ``redis.StrictRedis`` class grab default status we start to using it as
our default connection class.

To change this behavior or even use your own class for redis connection you
should pass a class itself or its path to ``REDIS_CLASS`` setting as::

    from redis import Redis
    REDIS_CLASS = Redis

or::

    REDIS_CLASS = 'redis.Redis'
    REDIS_CLASS = 'path.to.module.Redis'

REDIS_URL
---------

.. versionadded:: 0.2

Sometimes, your redis settings stored as ``redis://...`` url (like in Heroku
or DotCloud services), so you could to provide just ``REDIS_URL`` setting
and ``Flask-And-Redis`` auto parsed that value and will configure then valid
redis connection.

In case, when ``REDIS_URL`` provided all appropriate configurations, and other
keys are overwritten using their values at the present URI.

Config prefix
-------------

.. versionadded:: 0.4

Config prefix allows you to determine the set of configuration variables used
to configure ``redis.Redis`` connection. By default, config prefix ``REDIS``
would be used.

But when you want to initialize multiple redis connections, you could do this
like::

    from flask import flask
    from flask.ext.redis import Redis

    app = Flask(__app__)
    app.config['REDIS_HOST'] = 'localhost'
    app.config['REDIS_PORT'] = 6379
    app.config['REDIS_DB'] = 0
    redis1 = Redis(app)

    app.config['REDIS2_URL'] = 'redis://localhost:6379/1'
    redis2 = Redis(app, 'REDIS2')

API
===

.. module:: flask_redis

.. autoclass:: Redis
   :members:
   :special-members:
   :exclude-members: __weakref__

Changelog
=========

0.6 (Jan 8, 2015)
----------------------

* Python 3 support.
* Move documentation to Read the Docs.
* Refactor example test project to Comments app which shows how to use two
  Redis databases simultaneously.

0.5 (May 10, 2013)
------------------

* Use ``redis.StrictRedis`` as connection class by default.
* Understands unix socket path in ``REDIS_HOST``.
* Updates to README.

0.4 (Sep 29, 2012)
------------------

* Big refactor for :class:`~.Redis` class. Do not inherit ``redis.Redis`` class,
  store active redis connection in ``Redis.connection`` attribute and
  ``app.extensions['redis']`` dict.
* Add support of ``config_prefix`` keyword argument for :class:`~.Redis` or
  :meth:`~.Redis.init_app` methods.
* Support multiple redis connections in test application.

0.3.3 (Aug 29, 2012)
--------------------

* Fix problem while parsing ``REDIS_URL`` value, strip unnecessary slashes from
  database path (like ``redis://localhost:6379/12/``).

0.3.2 (Aug 15, 2012)
--------------------

* Added ``redis`` as install requirement in ``setup.py``.

0.3.1 (Jun 19, 2012)
--------------------

* Move from ``flask_redis`` package to python module.
* Little improvements for storing ``_flask_app`` attribute to :class:`~.Redis`
  instance.

0.3 (May 21, 2012)
------------------

* Implement :meth:`~.Redis.init_app` method.

0.2.1 (Mar 30, 2012)
--------------------

* Convert ``REDIS_PORT`` to an ``int`` instance.

0.2 (Mar 30, 2012)
------------------

* Added support of ``REDIS_URL`` setting. By default, :class:`~.Redis` will try
  to guess host, port, user, password and db settings from that value.

0.1 (Mar 12, 2012)
------------------

* Initial release.

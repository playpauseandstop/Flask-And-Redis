===============
Flask-And-Redis
===============

Simple as dead support of Redis database for Flask apps.

.. note:: I named this ``Flask-And-Redis``, cause ``Flask-Redis`` name already
   `taken <http://pypi.python.org/pypi/Flask-Redis>`_, but that library didn't
   match my needs.

Requirements
============

* `Python <http://www.python.org>`_ 2.6 or higher
* `Flask <http://flask.pocoo.org/>`_ 0.8 or higher
* `redis-py <https://github.com/andymccurdy/redis-py>`_ 2.4 or higher

Installation
============

::

    $ pip install Flask-And-Redis

License
=======

``Flask-And-Redis`` is licensed under the `BSD License
<https://github.com/playpauseandstop/Flask-And-Redis/blob/master/LICENSE>`_.

Configuration
=============

As of ``py-redis`` 2.4.11 and 2.6.0 releases you should setup next options in
your settings module:

* ``REDIS_HOST``
* ``REDIS_PORT``
* ``REDIS_DB``
* ``REDIS_PASSWORD``
* ``REDIS_SOCKET_TIMEOUT``
* ``REDIS_CONNECTION_POOL``
* ``REDIS_CHARSET``
* ``REDIS_ERRORS``
* ``REDIS_UNIX_SOCKET_PATH``

Later these values would initialize ``redis.Redis`` connection and all public
methods of that instance would be added to ``flask_redis.Redis`` instance for
easy use.

Also this connection would be stored in ``flask_redis.Redis.connection``
attribute and in ``app.extensions['redis']`` dict.

REDIS_URL
---------

.. versionadded:: 0.2

Some times, your redis settings stored as ``redis://...`` url (like in Heroku
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

So when you want to initialize several ``redis`` connections, you need to::

    from flask import flask
    from flask.ext.redis import Redis

    app = Flask(__app__)
    app.config['REDIS_HOST'] = 'localhost'
    app.config['REDIS_PORT'] = 6379
    app.config['REDIS_DB'] = 0
    redis1 = Redis(app)

    app.config['REDIS2_URL'] = 'redis://localhost:6379/1'
    redis2 = Redis(app, 'REDIS2')

Usage
=====

In regular case all of you need is import ``Redis`` instance and initialize it
with ``app`` instance, like::

    from flask import Flask
    from flask.ext.redis import Redis

    app = Flask(__name__)
    redis = Redis(app)

If you use application factories you could use ``init_app`` method,

.. versionadded:: 0.3

::

    redis = Redis()
    # The later on
    app = create_app('config.cfg')
    redis.init_app(app)

Also later you can get ``redis`` connection from ``app.extensions['redis']``
dict, where ``key`` is config prefix and ``value`` is worked redis connection
instance.

Bugs, feature requests?
=======================

If you found some bug in ``Flask-And-Redis`` library, please, add new issue to
the project's `GitHub issues
<https://github.com/playpauseandstop/Flask-And-Redis/issues>`_.

Changelog
=========

0.4
---

+ Big refactor of ``Redis`` instance. Do not inherit ``redis.Redis`` class,
  store active redis connection in ``Redis.connection`` attribute and
  ``app.extensions['redis']`` dict.
+ Add support of ``config_prefix`` keyword argument for ``Redis`` or
  ``init_app`` methods.
+ Support multiple redis connections in test application.

0.3.3
-----

+ Fix problem while parsing ``REDIS_URL`` value, strip unnecessary slashes from
  database path (like ``redis://localhost:6379/12/``).

0.3.2
-----

+ Checked compability with ``redis-py`` version 2.6.0.
+ Added ``redis`` as install requirement in ``setup.py``.

0.3.1
-----

+ Move from ``flask_redis`` package to python module.
+ Little improvements for storing ``_flask_app`` attribute to ``Redis``
  instance.

0.3
---

+ Implement ``init_app`` method.

0.2.1
-----

+ Convert ``REDIS_PORT`` to an ``int`` instance.

0.2
---

+ Added support of ``REDIS_URL`` setting. By default, ``Redis`` will try to
  guess host, port, user, password and db settings from that value.

0.1
---

* Initial release.

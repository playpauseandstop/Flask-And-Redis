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

As of ``py-redis`` 2.4.11 release you should setup next options in your
settings module:

* ``REDIS_HOST``
* ``REDIS_PORT``
* ``REDIS_DB``
* ``REDIS_PASSWORD``
* ``REDIS_SOCKET_TIMEOUT``
* ``REDIS_CONNECTION_POOL``
* ``REDIS_CHARSET``
* ``REDIS_ERRORS``
* ``REDIS_UNIX_SOCKET_PATH``

Then all of these args would be sent to ``redis.Redis.__init__`` method.

You also could pass app into initialized instance afterwards with ``init_app``
method::

    from flask import Flask
    from flask.ext.redis import Redis


    app = Flask(__name__)

    redis = Redis()
    redis.init_app(app)

.. warning:: Please note, if you'll initialize extension that way, make sure
   that before ``init_app`` call all real Redis method's would be return
   ``AttributeError`` exception cause of no ``connection_pool`` attribute,
   which setup on ``redis.Redis`` instance init.

Advanced
--------

Some times, your redis setting stored as ``redis://...`` url (like in Heroku
or DotCloud services), sou you could to provide just ``REDIS_URL`` value
and ``Flask-And-Redis`` auto parsed that url and configured then valid redis
connection.

Usage
=====

Basic
-----

::

    from flask import Flask
    from flask.ext.redis import Redis


    app = Flask(__name__)
    redis = Redis(app)

Test application
----------------

``testapp/app.py``

::

    from flask import Flask, redirect, url_for
    from flask.ext.redis import Redis

    from testapp import settings


    # Initialize simple Flask application
    app = Flask(__name__)
    app.config.from_object(settings)

    # Setup Redis conection
    redis = Redis(app)

    # Add two simple views: One for forgetting counter
    @app.route('/forget-us')
    def forget_us():
        key = app.config['COUNTER_KEY']
        redis.delete(key)
        return redirect(url_for('home'))


    # Second for remembering visiting counter
    @app.route('/')
    def home():
        key = app.config['COUNTER_KEY']
        counter = redis.incr(key)
        message = 'Hello, visitor!'

        if counter != 1:
            message += "\nThis page viewed %d time(s)." % counter

        return message

----

``testapp/settings.py``

::

    COUNTER_KEY = 'testapp:counter'
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
    # REDIS_URL = 'redis://localhost:6379/0'

Bugs, feature requests?
=======================

If you found some bug in ``Flask-And-Redis`` library, please, add new issue to
the project's `GitHub issues
<https://github.com/playpauseandstop/Flask-And-Redis/issues>`_.

Changelog
=========

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

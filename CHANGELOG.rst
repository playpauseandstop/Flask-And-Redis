1.0.0 (2019-02-18)
------------------

* Drop Python 2.6 & 3.3 support, ensure Python 3.6+ support. Kudos to
  `jezdez <https://github.com/jezdez>`_ for pull request & implementation
* Support subclasses of the Redis client class. Again kudos to
  `jezdez  <https://github.com/jezdez>`_ for pull request & implementation
* Use `inspect.getfullargspec()` if available. Kudos to
  `vibiu <https://github.com/vibiu>`_ for pull request & implementation
* Use `redis.Redis` as default connection class, when using
  `redis-py <https://github.com/andymccurdy/redis-py>`_ >= 3

0.7 (2016-11-12)
----------------

* Improve multiple app support. Kudos to
  `timothyqiu <https://github.com/timothyqiu>`_ for pull request &
  implementation
* Simplify running tests for test application

0.6 (2015-01-08)
----------------

* Python 3 support.
* Move documentation to Read the Docs.
* Refactor example test project to Comments app which shows how to use two
  Redis databases simultaneously.

0.5 (2013-05-10)
------------------

* Use ``redis.StrictRedis`` as connection class by default.
* Understands unix socket path in ``REDIS_HOST``.
* Updates to README.

0.4 (2012-09-29)
----------------

* Big refactor for :class:`~.Redis` class. Do not inherit ``redis.Redis`` class,
  store active redis connection in ``Redis.connection`` attribute and
  ``app.extensions['redis']`` dict.
* Add support of ``config_prefix`` keyword argument for :class:`~.Redis` or
  :meth:`~.Redis.init_app` methods.
* Support multiple redis connections in test application.

0.3.3 (2012-08-29)
------------------

* Fix problem while parsing ``REDIS_URL`` value, strip unnecessary slashes from
  database path (like ``redis://localhost:6379/12/``).

0.3.2 (2012-08-15)
------------------

* Added ``redis`` as install requirement in ``setup.py``.

0.3.1 (2012-06-19)
--------------------

* Move from ``flask_redis`` package to python module.
* Little improvements for storing ``_flask_app`` attribute to :class:`~.Redis`
  instance.

0.3 (2012-05-21)
----------------

* Implement :meth:`~.Redis.init_app` method.

0.2.1 (2012-03-30)
------------------

* Convert ``REDIS_PORT`` to an ``int`` instance.

0.2 (2012-03-30)
----------------

* Added support of ``REDIS_URL`` setting. By default, :class:`~.Redis` will try
  to guess host, port, user, password and db settings from that value.

0.1 (2012-03-12)
----------------

* Initial release.

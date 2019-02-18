"""
===========
flask_redis
===========

Simple as dead support of Redis database for Flask apps.

"""

import inspect
import sys

try:
    import urllib.parse as urlparse
except ImportError:  # pragma: no cover
    import urlparse

try:
    from flask import _app_ctx_stack
except ImportError:  # pragma: no cover
    _app_ctx_stack = None

import redis
from flask import _request_ctx_stack
from werkzeug.utils import import_string


__all__ = ('Redis', )


__author = 'Igor Davydenko'
__license__ = 'BSD License'
__version__ = '1.0.0'


IS_PY3 = sys.version_info[0] == 3
IS_REDIS3 = redis.VERSION[0] == 3
string_types = (str if IS_PY3 else basestring, )  # noqa

# Default Redis connection class
RedisClass = redis.Redis if IS_REDIS3 else redis.StrictRedis

# Which stack should we use? _app_ctx_stack is new in 0.9
connection_stack = _app_ctx_stack or _request_ctx_stack


class Redis(object):

    """Simple as dead support of Redis database for Flask apps."""

    def __init__(self, app=None, config_prefix=None):
        """Initialize Redis extension for Flask application.

        If ``app`` argument provided then initialize redis connection using
        application config values.

        If no ``app`` argument provided you should do initialization later with
        :meth:`init_app` method.

        Generally extension expects configuration to be prefixed with ``REDIS``
        config prefix, to customize things pass different ``config_prefix``
        here or on calling :meth:`init_app` method. For example, if you have
        URL to Redis in ``CACHE_URL`` config key, you should pass
        ``config_prefix='CACHE'`` to extension.

        :param app: :class:`flask.Flask` application instance.
        :param config_prefix: Config prefix to use. By default: ``REDIS``
        """
        self.app = app

        if app is not None:
            self.init_app(app, config_prefix)

    @property
    def connection(self):
        """Return Redis connection for current app."""
        return self.get_app().extensions['redis'][self.config_prefix]

    def get_app(self):
        """Get current app from Flast stack to use.

        This will allow to ensure which Redis connection to be used when
        accessing Redis connection public methods via plugin.
        """
        # First see to connection stack
        ctx = connection_stack.top
        if ctx is not None:
            return ctx.app

        # Next return app from instance cache
        if self.app is not None:
            return self.app

        # Something went wrong, in most cases app just not instantiated yet
        # and we cannot locate it
        raise RuntimeError(
            'Flask application not registered on Redis instance '
            'and no applcation bound to current context')

    def init_app(self, app, config_prefix=None):
        """
        Actual method to read redis settings from app configuration, initialize
        Redis connection and copy all public connection methods to current
        instance.

        :param app: :class:`flask.Flask` application instance.
        :param config_prefix: Config prefix to use. By default: ``REDIS``
        """
        # Put redis to application extensions
        if 'redis' not in app.extensions:
            app.extensions['redis'] = {}

        # Which config prefix to use, custom or default one?
        self.config_prefix = config_prefix = config_prefix or 'REDIS'

        # No way to do registration two times
        if config_prefix in app.extensions['redis']:
            raise ValueError('Already registered config prefix {0!r}.'.
                             format(config_prefix))

        # Start reading configuration, define converters to use and key func
        # to prepend config prefix to key value
        converters = {'port': int}
        convert = lambda arg, value: (converters[arg](value)
                                      if arg in converters
                                      else value)
        key = lambda param: '{0}_{1}'.format(config_prefix, param)

        # Which redis connection class to use?
        klass = app.config.get(key('CLASS'), RedisClass)

        # Import connection class if it stil path notation
        if isinstance(klass, string_types):
            klass = import_string(klass)

        # Should we use URL configuration
        url = app.config.get(key('URL'))

        # If should, parse URL and store values to application config to later
        # reuse if necessary
        if url:
            urlparse.uses_netloc.append('redis')
            url = urlparse.urlparse(url)

            # URL could contains host, port, user, password and db values
            app.config[key('HOST')] = url.hostname
            app.config[key('PORT')] = url.port or 6379
            app.config[key('USER')] = url.username
            app.config[key('PASSWORD')] = url.password
            db = url.path.replace('/', '')
            app.config[key('DB')] = db if db.isdigit() else None

        # Host is not a mandatory key if you want to use connection pool. But
        # when present and starts with file:// or / use it as unix socket path
        host = app.config.get(key('HOST'))
        if host and (host.startswith('file://') or host.startswith('/')):
            app.config.pop(key('HOST'))
            app.config[key('UNIX_SOCKET_PATH')] = host

        args = self._build_connection_args(klass)
        kwargs = dict([(arg, convert(arg, app.config[key(arg.upper())]))
                       for arg in args
                       if key(arg.upper()) in app.config])

        # Initialize connection and store it to extensions
        connection = klass(**kwargs)
        app.extensions['redis'][config_prefix] = connection

        # Include public methods to current instance
        self._include_public_methods(connection)

    def _build_connection_args(self, klass):
        """Read connection args spec, exclude self from list of possible

        :param klass: Redis connection class.
        """
        bases = [base for base in klass.__bases__ if base is not object]
        all_args = []
        for cls in [klass] + bases:
            try:
                args = inspect.getfullargspec(cls.__init__).args
            except AttributeError:
                args = inspect.getargspec(cls.__init__).args
            for arg in args:
                if arg in all_args:
                    continue
                all_args.append(arg)
        all_args.remove('self')
        return all_args

    def _include_public_methods(self, connection):
        """Include public methods from Redis connection to current instance.

        :param connection: Redis connection instance.
        """
        for attr in dir(connection):
            value = getattr(connection, attr)
            if attr.startswith('_') or not callable(value):
                continue
            self.__dict__[attr] = self._wrap_public_method(attr)

    def _wrap_public_method(self, attr):
        """
        Ensure that plugin will call current connection method when accessing
        as ``plugin.<public_method>(*args, **kwargs)``.
        """
        def wrapper(*args, **kwargs):
            return getattr(self.connection, attr)(*args, **kwargs)
        return wrapper

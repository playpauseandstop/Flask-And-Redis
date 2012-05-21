import inspect
import urlparse

from redis import Redis as BaseRedis


__all__ = ('Redis', )


class Redis(BaseRedis):
    """
    Simple object to initialize redis client using settings from Flask
    application.
    """
    def __init__(self, app=None):
        """
        Overwrite default ``Redis.__init__`` method, read all necessary
        settings from Flask app config instead of positional and keyword args.

        The possible settings are:

        * REDIS_HOST
        * REDIS_PORT
        * REDIS_DB
        * REDIS_PASSWORD
        * REDIS_SOCKET_TIMEOUT
        * REDIS_CONNECTION_POOL
        * REDIS_CHARSET
        * REDIS_ERRORS
        * REDIS_UNIX_SOCKET_PATH

        You also could initialize ``Redis`` instance without sending ``app``
        object, but do this after with ``init_app`` method, like::

            from flask import Flask
            from flask.ext.redis import Redis

            app = Flask(__name__)

            redis = Redis()
            redis.init_app(app)

        .. warning:: Please note, if you'll initialize extension that way, make
           sure that before ``init_app`` call all real Redis method's would be
           return ``AttributeError`` exception cause of no ``connection_pool``
           attribute, which setup on ``Redis`` instance init.

        Advanced usage
        --------------

        If you want to use this extension on Heroku or other build services
        where redis URL stored in environment var you could to determine full
        URL to redis server.

        For example, for Heroku apps which used ``REDISTOGO_URL`` environ app,
        you'll need to update your project settings with::

            import os

            REDIS_URL = 'redis://localhost:6379/0'
            REDIS_URL = os.environ.get('REDISTOGO_URL', REDIS_URL)

        """
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Actual method to read redis settings from app configuration.
        """
        converters = {'port': int}
        url = app.config.get('REDIS_URL')

        if url:
            urlparse.uses_netloc.append('redis')
            url = urlparse.urlparse(url)

            # URL could contains host, port, user, password and db
            # values. Store their to config
            app.config['REDIS_HOST'] = url.hostname
            app.config['REDIS_PORT'] = url.port
            app.config['REDIS_USER'] = url.username
            app.config['REDIS_PASSWORD'] = url.password
            app.config['REDIS_DB'] = \
                url.path if url.path.isdigit() else None

        spec = inspect.getargspec(BaseRedis.__init__)
        args = set(spec.args).difference(set(['self']))
        kwargs = {}

        for arg in args:
            redis_arg = 'REDIS_%s' % arg.upper()

            if not redis_arg in app.config:
                continue

            value = app.config.get(redis_arg)

            if arg in converters:
                value = converters[arg](value)

            kwargs.update({arg: value})

        super(Redis, self).__init__(**kwargs)
        setattr(self, '_flask_app', app)

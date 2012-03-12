import inspect

from redis import Redis as BaseRedis


__all__ = ('Redis', )


class Redis(BaseRedis):
    """
    Simple object to initialize redis client using settings from Flask
    application.
    """
    def __init__(self, app):
        """
        Overwrite default ``Redis.__init__`` method, read all necessary
        settings from Flask app instead of positional and keyword args.

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

        """
        spec = inspect.getargspec(BaseRedis.__init__)
        args = set(spec.args).difference(set(['self']))
        kwargs = {}

        for arg in args:
            redis_arg = 'REDIS_%s' % arg.upper()

            if not redis_arg in app.config:
                continue

            kwargs.update({arg: app.config.get(redis_arg)})

        super(Redis, self).__init__(**kwargs)
        setattr(self, '_flask_app', app)

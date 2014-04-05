"""
==============================
testapp.tests.test_flask_redis
==============================

Test Flask-And-Redis extension.

"""

from flask.ext.redis import Redis
from redis import StrictRedis
from redis.exceptions import ConnectionError

from app import redis as default_redis

from .common import TestCase


class CustomRedis(StrictRedis):
    """
    Custom Redis class based on ``StrictRedis``.
    """


class TestFlaskRedis(TestCase):

    MULTIPLE_REDIS_SERVERS = False

    def setUp(self):
        for name, value in self.app.config.items():
            if not name.startswith('REDIS_'):
                continue
            setattr(self, name, value)

    def tearDown(self):
        config_items = self.app.config.items()

        if 'redis' in self.app.extensions:
            self.app.extensions['redis'].pop('REDIS2', None)
            self.app.extensions['redis'].pop('REDIS3', None)
            self.app.extensions['redis'].pop('REDIS_BACKUP', None)
            self.app.extensions['redis'].pop('REDIS_SLAVE', None)

        for name, value in config_items:
            if not name.startswith('REDIS_') or not name.endswith('_URL'):
                continue
            self.app.config.pop(name)

    def test_config_prefix(self):
        redis = Redis(self.app, 'REDIS_BACKUP')
        self.assertIn('REDIS_BACKUP', self.app.extensions['redis'])
        redis.ping()
        self.assertRaises(ValueError, Redis, self.app, 'REDIS_BACKUP')

        redis = Redis()
        redis.init_app(self.app, 'REDIS_SLAVE')
        self.assertIn('REDIS_SLAVE', self.app.extensions['redis'])
        redis.ping()
        self.assertRaises(ValueError, redis.init_app, self.app, 'REDIS_SLAVE')

    def test_config_prefix_url(self):
        self.app.config['REDIS2_URL'] = 'redis://localhost:6379/0'
        redis = Redis(self.app, 'REDIS2')
        redis.ping()

        self.app.config['REDIS3_URL'] = 'redis://127.0.0.1:6379/0'
        redis = Redis()
        redis.init_app(self.app, 'REDIS3')
        redis.ping()

    def test_config_prefix_wrong_config(self):
        self.app.config['REDIS_BACKUP_HOST'] = 'wrong-host'
        self.app.config['REDIS_BACKUP_PORT'] = 8080
        self.app.config['REDIS_BACKUP_DB'] = 9

        redis = Redis(self.app, 'REDIS_BACKUP')
        self.assertRaises(ConnectionError, redis.ping)

    def test_config_prefix_wrong_url(self):
        self.app.config['REDIS2_URL'] = 'redis://wrong-host:8080/9'
        redis = Redis(self.app, 'REDIS2')
        self.assertRaises(ConnectionError, redis.ping)

        self.app.config['REDIS3_URL'] = 'redis://wrong-host:8080/9'
        redis = Redis()
        redis.init_app(self.app, 'REDIS3')
        self.assertRaises(ConnectionError, redis.ping)

    def test_connection_class(self):
        self.app.config['REDIS_CUSTOM_CLASS'] = CustomRedis
        self.app.config['REDIS_CUSTOM_URL'] = 'redis://localhost:6379/0'
        redis = Redis(self.app, 'REDIS_CUSTOM')
        redis.ping()

        self.app.extensions['redis'].pop('REDIS_CUSTOM')
        self.app.config['REDIS_CUSTOM_CLASS'] = 'redis.Redis'
        redis = Redis(self.app, 'REDIS_CUSTOM')
        redis.ping()

    def test_default_behaviour(self):
        self.assertEqual(default_redis.config_prefix, 'REDIS')
        default_redis.ping()
        self.assertIn('redis', self.app.extensions)

        redis = self.app.extensions['redis']['REDIS']
        self.assertEqual(default_redis.connection, redis)
        redis.ping()

    def test_init_app(self):
        self.assertIn('redis', self.app.extensions)
        self.app.extensions.pop('redis')

        redis = Redis()
        self.assertFalse(hasattr(redis, 'ping'))
        redis.init_app(self.app)
        redis.ping()

    def test_init_app_url(self):
        self.app.extensions.pop('redis')

        self.app.config.pop('REDIS_HOST')
        self.app.config.pop('REDIS_PORT')
        self.app.config.pop('REDIS_DB')

        self.app.config['REDIS_URL'] = 'redis://localhost:6379/0'
        redis = Redis()
        redis.init_app(self.app)
        redis.ping()

    def test_init_app_wrong_config(self):
        self.app.extensions.pop('redis')

        self.app.config['REDIS_HOST'] = 'wrong-host'
        self.app.config['REDIS_PORT'] = 8080
        self.app.config['REDIS_DB'] = 9

        redis = Redis()
        redis.init_app(self.app)
        self.assertRaises(ConnectionError, redis.ping)

    def test_init_app_wrong_url(self):
        self.app.extensions.pop('redis')
        self.app.config['REDIS_URL'] = 'redis://wrong-host:8080/9'

        redis = Redis()
        redis.init_app(self.app)
        self.assertRaises(ConnectionError, redis.ping)

    def test_redis_methods(self):
        attributes = dir(default_redis)
        instance = self.app.extensions['redis']['REDIS']

        for attr in dir(instance):
            if attr.startswith('_') or not callable(getattr(instance, attr)):
                continue
            self.assertIn(attr, attributes)

    def test_unix_socket_path(self):
        self.app.config['REDIS_CUSTOM_HOST'] = '/does/not/exist/redis.sock'
        redis = Redis(self.app, 'REDIS_CUSTOM')
        self.assertRaisesRegexp(ConnectionError, 'unix socket', redis.ping)

    def test_url(self):
        self.app.extensions.pop('redis')
        self.app.config['REDIS_URL'] = 'redis://localhost:6379/0'
        redis = Redis(self.app)
        redis.ping()

    def test_url_default_port(self):
        self.app.extensions.pop('redis')
        self.app.config['REDIS_URL'] = 'redis://localhost/0'
        redis = Redis(self.app)
        redis.ping()

    def test_wrong_config(self):
        self.app.extensions.pop('redis')

        self.app.config['REDIS_HOST'] = 'wrong-host'
        self.app.config['REDIS_PORT'] = 8080
        self.app.config['REDIS_DB'] = 9

        redis = Redis(self.app)
        self.assertRaises(ConnectionError, redis.ping)

    def test_wrong_url(self):
        self.app.extensions.pop('redis')
        self.app.config['REDIS_URL'] = 'redis://wrong-host:8080/9'
        redis = Redis(self.app)
        self.assertRaises(ConnectionError, redis.ping)

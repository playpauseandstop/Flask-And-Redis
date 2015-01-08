"""
=============
testapp.tests
=============

Tests for Flask-And-Redis extension and for Comments app.

"""

from unittest import TestCase

from flask import Flask
from flask_redis import Redis
from redis import StrictRedis
from redis.connection import UnixDomainSocketConnection


TEST_REDIS_DB = 0
TEST_REDIS_HOST = '127.0.0.1'
TEST_REDIS_PORT = 6379
TEST_REDIS_URL = 'redis://127.0.0.1:6379/0'


class InheritFromStrictRedis(StrictRedis):

    """Dummy class inherited from Strict Redis."""


class TestFlaskAndRedis(TestCase):

    def create_app(self, **options):
        defaults = {'TESTING': True}
        defaults.update(options)

        app = Flask('testapp')
        app.config.update(defaults)

        return app

    def test_already_registered(self):
        app = self.create_app(REDIS_URL=TEST_REDIS_URL)
        Redis(app)
        self.assertRaises(ValueError, Redis, app)

    def test_class(self):
        app = self.create_app(REDIS_CLASS=InheritFromStrictRedis,
                              REDIS_URL=TEST_REDIS_URL)
        redis = Redis(app)
        redis.ping()

    def test_class_from_string(self):
        app = self.create_app(REDIS_CLASS='redis.Redis',
                              REDIS_URL=TEST_REDIS_URL)
        redis = Redis(app)
        redis.ping()

    def test_config_prefix(self):
        redis_url = TEST_REDIS_URL.replace('/0', '/1')
        app = self.create_app(REDIS_URL=TEST_REDIS_URL,
                              REDIS1_URL=redis_url)

        redis = Redis(app)
        redis.ping()

        redis1 = Redis(app, 'REDIS1')
        redis1.ping()

    def test_default_behaviour(self):
        app = self.create_app(REDIS_HOST=TEST_REDIS_HOST,
                              REDIS_PORT=TEST_REDIS_PORT,
                              REDIS_DB=TEST_REDIS_DB)
        redis = Redis(app)
        redis.ping()

    def test_init_app_behaviour(self):
        redis = Redis()
        self.assertRaises(AttributeError, getattr, redis, 'ping')

        app = self.create_app(REDIS_HOST=TEST_REDIS_HOST,
                              REDIS_PORT=TEST_REDIS_PORT,
                              REDIS_DB=TEST_REDIS_DB)

        redis.init_app(app)
        redis.ping()

    def test_non_string_port(self):
        app = self.create_app(REDIS_HOST=TEST_REDIS_HOST,
                              REDIS_PORT=str(TEST_REDIS_PORT),
                              REDIS_DB=str(TEST_REDIS_DB))
        redis = Redis(app)
        redis.ping()

    def test_socket_path_in_host(self, host=None):
        host = host or '/var/lib/redis/run.sock'
        app = self.create_app(REDIS_HOST=host)

        redis = Redis(app)
        self.assertFalse(hasattr(redis, 'connection_pool'))

        real_redis = app.extensions['redis']['REDIS']
        self.assertEqual(
            real_redis.connection_pool.connection_class,
            UnixDomainSocketConnection
        )

    def test_socket_path_in_host_started_with_file(self):
        self.test_socket_path_in_host('file:///tmp/run.sock')

    def test_url(self):
        app = self.create_app(REDIS_URL='redis://127.0.0.1:6379/0')
        redis = Redis(app)
        redis.ping()

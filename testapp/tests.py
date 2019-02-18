"""
=============
testapp.tests
=============

Tests for Flask-And-Redis extension and for Comments app.

"""

from unittest import TestCase

import flask_redis
import redis as redis_py
from flask import Flask, url_for
from flask_redis import Redis
from flask_testing import TestCase as FlaskTestCase
from nose.plugins.attrib import attr
from redis import StrictRedis
from redis.connection import UnixDomainSocketConnection

from app import create_app


TEST_REDIS_DB = 0
TEST_REDIS_HOST = '127.0.0.1'
TEST_REDIS_PORT = 6379
TEST_REDIS_URL = 'redis://127.0.0.1:6379/0'
TEST_USERNAME = 'test-username'

udata = lambda response: response.data.decode(response.charset)


class InheritFromStrictRedis(StrictRedis):

    """Dummy class inherited from Strict Redis."""


class CustomInitStrictRedis(StrictRedis):
    """Dummy class that has own __init__ defined"""

    def __init__(self, foo="bar", *args, **kwargs):
        super(CustomInitStrictRedis, self).__init__(*args, **kwargs)
        self.foo = foo


def get_context(app):
    creator = getattr(app, 'app_context', app.test_request_context)
    return creator()


@attr('testapp')
class TestCommentsApp(FlaskTestCase):

    KEY_PREFIX = 'test:far_testapp'
    TESTING = True

    def setUp(self):
        self.index_url = url_for('index')
        self.quit_url = url_for('quit')
        self.start_thread_url = url_for('start_thread')
        self.threads_url = url_for('threads')

    def check_logged_in(self, username=None):
        username = username or TEST_USERNAME
        response = self.client.get(self.threads_url)
        self.assert200(response)
        self.assertIn('<strong>{0}</strong>'.format(username), udata(response))

    def check_not_logged_in(self):
        response = self.client.get(self.threads_url)
        self.assertRedirects(response, self.index_url)

    def create_app(self):
        return create_app()

    def test_error_handling(self):
        response = self.client.get('/does-not-exist.exe')
        self.assert404(response)

    def test_index(self):
        response = self.client.get(self.index_url)
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        self.assertContext('error', None)

    def test_login(self):
        response = self.client.post(self.index_url,
                                    data={'username': TEST_USERNAME})
        self.assertRedirects(response, self.threads_url)
        self.check_logged_in()

    def test_login_failed(self):
        response = self.client.post(self.index_url, data={'username': ''})
        self.assert400(response)
        self.assertTemplateUsed('index.html')
        self.assertContext('error', True)

    def test_quit(self):
        self.test_login()

        response = self.client.get(self.quit_url)
        self.assertRedirects(response, self.index_url)

        self.check_not_logged_in()

    def test_quit_not_logged_in(self):
        self.check_not_logged_in()
        response = self.client.get(self.quit_url)
        self.assertRedirects(response, self.index_url)


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

    def test_class_custom_init(self):
        app = self.create_app(REDIS_CLASS=CustomInitStrictRedis,
                              REDIS_URL='redis://127.0.0.1:6379/1')
        redis = Redis(app)
        redis.ping()
        self.assertEqual(redis.connection.foo, "bar")
        self.assertEqual(
            redis.connection.connection_pool.connection_kwargs['db'], '1'
        )

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

    def test_default_class_redis_3(self):
        app = self.create_app(REDIS_URL=TEST_REDIS_URL)

        redis = Redis(app)
        real_redis = app.extensions['redis']['REDIS']

        self.assertIsInstance(
            real_redis,
            redis_py.Redis if flask_redis.IS_REDIS3 else StrictRedis)

    def test_init_app_behaviour(self):
        redis = Redis()
        self.assertRaises(AttributeError, getattr, redis, 'ping')

        app = self.create_app(REDIS_HOST=TEST_REDIS_HOST,
                              REDIS_PORT=TEST_REDIS_PORT,
                              REDIS_DB=TEST_REDIS_DB)

        redis.init_app(app)

        # Extensions initialized by init_app are not bound to any app
        # So you need an application context to access it
        self.assertRaises(RuntimeError, redis.ping)
        with get_context(app):
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


class TestMultipleAppSupport(TestCase):
    def setUp(self):
        self.redis = redis = Redis()
        self.app_a = self.create_app(REDIS_URL='redis://127.0.0.1:6379/0',
                                     REDIS_DECODE_RESPONSES=True)
        self.app_b = self.create_app(REDIS_URL='redis://127.0.0.1:6379/1',
                                     REDIS_DECODE_RESPONSES=True)
        redis.init_app(self.app_a)
        redis.init_app(self.app_b)

    def create_app(self, **options):
        defaults = {'TESTING': True}
        defaults.update(options)

        app = Flask('testapp')
        app.config.update(defaults)

        return app

    def test_connections(self):
        with get_context(self.app_a):
            self.redis.ping()
        with get_context(self.app_b):
            self.redis.ping()

    def test_different_values(self):
        key = 'test:flask_redis:foo'
        value_a = 'foo'
        value_b = 'bar'

        # Set key to different values in different apps
        with get_context(self.app_a):
            self.redis.set(key, value_a)
        with get_context(self.app_b):
            self.redis.set(key, value_b)

        # Get key should produce different values in different apps
        with get_context(self.app_a):
            self.assertEqual(self.redis.get(key), value_a)
        with get_context(self.app_b):
            self.assertEqual(self.redis.get(key), value_b)

#!/usr/bin/env python

import unittest

# Simple manipulation to use ``unittest2`` if current Python version is
# less than 2.7
if not hasattr(unittest.TestCase, 'assertIn'):
    import unittest2 as unittest

from flask import url_for
from flask.ext.redis import Redis
from redis.exceptions import ConnectionError

from app import app, redis


class TestFlaskRedis(unittest.TestCase):

    def setUp(self):
        self.old_COUNTER_KEY = app.config['COUNTER_KEY']
        self.old_REDIS_HOST = app.config['REDIS_HOST']
        self.old_REDIS_PORT = app.config['REDIS_PORT']
        self.old_REDIS_DB = app.config['REDIS_DB']

        app.config['COUNTER_KEY'] += '_test'
        app.config['TESTING'] = True

        self.app = app.test_client()

        self.forget_us_url = self.url('forget_us')
        self.home_url = self.url('home')

    def tearDown(self):
        redis.delete(app.config['COUNTER_KEY'])

        app.config.pop('REDIS_URL', None)

        app.config['COUNTER_KEY'] = self.old_COUNTER_KEY
        app.config['REDIS_HOST'] = self.old_REDIS_HOST
        app.config['REDIS_PORT'] = self.old_REDIS_PORT
        app.config['REDIS_DB'] = self.old_REDIS_DB
        app.config['TESTING'] = False

    def url(self, *args, **kwargs):
        with app.test_request_context():
            return url_for(*args, **kwargs)

    def test_custom_behaviour(self):
        app.config['REDIS_HOST'] = 'wrong-host'
        app.config['REDIS_PORT'] = 8080
        app.config['REDIS_DB'] = 0

        obj = Redis(app)
        self.assertRaises(ConnectionError, obj.ping)

    def test_custom_behaviour_init_app(self):
        app.config['REDIS_HOST'] = 'wrong-host'
        app.config['REDIS_PORT'] = 8080
        app.config['REDIS_DB'] = 0

        obj = Redis()
        self.assertRaises(AttributeError, obj.ping)

        obj.init_app(app)
        self.assertRaises(ConnectionError, obj.ping)

    def test_custom_behaviour_url(self):
        app.config['REDIS_URL'] = 'redis://wrong-host:8080/0'

        obj = Redis(app)
        self.assertRaises(ConnectionError, obj.ping)

    def test_custom_behaviour_url_init_app(self):
        app.config['REDIS_URL'] = 'redis://wrong-host:8080/0'

        obj = Redis()
        self.assertRaises(AttributeError, obj.ping)

        obj.init_app(app)
        self.assertRaises(ConnectionError, obj.ping)

    def test_default_behaviour(self):
        response = self.app.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Hello, visitor!')

        response = self.app.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data, 'Hello, visitor!\nThis page viewed 2 time(s).'
        )

        self.assertTrue(redis.exists(app.config['COUNTER_KEY']))

        response = self.app.get(self.forget_us_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers['Location'].endswith(self.home_url))

        self.assertFalse(redis.exists(app.config['COUNTER_KEY']))

        response = self.app.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Hello, visitor!')

    def test_default_behaviour_string_port(self):
        app.config['REDIS_PORT'] = str(app.config['REDIS_PORT'])

        obj = Redis(app)
        obj.ping()

    def test_default_behaviour_url(self):
        host = app.config.pop('REDIS_HOST')
        port = app.config.pop('REDIS_PORT')
        db = app.config.pop('REDIS_DB')

        app.config['REDIS_URL'] = 'redis://%s:%d/%d' % (host, port, db)

        obj = Redis(app)
        obj.ping()

    def test_default_behaviour_url_init_app(self):
        host = app.config.pop('REDIS_HOST')
        port = app.config.pop('REDIS_PORT')
        db = app.config.pop('REDIS_DB')

        app.config['REDIS_URL'] = 'redis://%s:%d/%d' % (host, port, db)

        obj = Redis()
        self.assertRaises(AttributeError, obj.ping)

        obj.init_app(app)
        obj.ping()


if __name__ == '__main__':
    unittest.main()

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
from scenarios.default import SCENARIO


class TestCase(unittest.TestCase):

    def setUp(self):
        self.old_REDIS_HOST = app.config['REDIS_HOST']
        self.old_REDIS_PORT = app.config['REDIS_PORT']
        self.old_REDIS_DB = app.config['REDIS_DB']

        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        app.config.pop('REDIS_URL', None)

        app.config['REDIS_HOST'] = self.old_REDIS_HOST
        app.config['REDIS_PORT'] = self.old_REDIS_PORT
        app.config['REDIS_DB'] = self.old_REDIS_DB
        app.config['TESTING'] = False

    def url(self, *args, **kwargs):
        with app.test_request_context():
            return url_for(*args, **kwargs)


class TestFlaskRedis(TestCase):

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


class TestViews(TestCase):

    def setUp(self):
        super(TestViews, self).setUp()

        self.home_url = self.url('home')
        self.test_url = self.url('test')

    def test_home(self):
        response = self.app.get(self.home_url)
        self.assertIn('<h1>Flask-And-Redis test project</h1>', response.data)

        self.assertIn('>Redis information</h2>', response.data)
        self.assertIn('>Server</th>', response.data)
        self.assertIn('>Clients</th>', response.data)
        self.assertIn('>Memory</th>', response.data)
        self.assertIn('>Stats</th>', response.data)
        self.assertIn('>CPU</th>', response.data)
        self.assertIn('>Other</th>', response.data)

        self.assertIn('>Test Redis server</h2>', response.data)
        self.assertIn('>Scenario type</label>', response.data)
        self.assertIn('>Scenario</label>', response.data)

    def test_test(self):
        data = {'scenario': 'ping\ninfo', 'scenario_type': 'redis'}
        response = self.app.post(self.test_url, data=data)
        self.assertIn('<h1>Flask-And-Redis test project</h1>', response.data)

        self.assertIn('<h2>Scenario successfully executed</h2>', response.data)
        self.assertIn('&gt; redis.ping()', response.data)
        self.assertIn('True', response.data)
        self.assertIn('&gt; redis.info()', response.data)

    def test_default(self):
        data = {'scenario': SCENARIO, 'scenario_type': 'redis'}
        response = self.app.post(self.test_url, data=data)
        self.assertIn('<h2>Scenario successfully executed</h2>', response.data)

    def test_test_errors(self):
        response = self.app.post(self.test_url, data={})
        self.assertIn('<h1>Flask-And-Redis test project</h1>', response.data)

        self.assertIn('>Error</h2>', response.data)
        self.assertIn(
            'One of required fields is not set. Please, check POST request '
            'or try again later.',
            response.data
        )

        data = {'scenario': 'pong', 'scenario_type': 'redis'}
        response = self.app.post(self.test_url, data=data)

        self.assertIn('>Error</h2>', response.data)
        self.assertIn(
            'Cannot convert redis scenario to Python, error is: ',
            response.data
        )

        data = {'scenario': 'redis.pong()', 'scenario_type': 'python'}
        response = self.app.post(self.test_url, data=data)

        self.assertIn('>Error</h2>', response.data)
        self.assertIn(
            'Error while executing Python scenario, error is: ',
            response.data
        )

    def test_test_redirect(self):
        response = self.app.get(self.test_url)
        self.assertEqual(response._status_code, 302)
        self.assertEqual(response.location, self.url('home', _external=True))


if __name__ == '__main__':
    unittest.main()

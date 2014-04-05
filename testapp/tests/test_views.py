"""
========================
testapp.tests.test_views
========================

Test web UI for Flask-And-Redis test project.

"""

from flask import url_for
from sandbox import Sandbox
from sandbox.recursion import SetRecursionLimit

from scenarios.default import SCENARIO

from .common import TestCase


Sandbox.PROTECTIONS.remove(SetRecursionLimit)


class TestViews(TestCase):

    def setUp(self):
        self.home_url = self.url('home')
        self.test_url = self.url('test')

    def url(self, url_rule, *args, **kwargs):
        return url_for(url_rule, *args, **kwargs)

    def test_home(self):
        response = self.client.get(self.home_url)
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
        data = {'scenario': 'ping\ninfo',
                'scenario_type': 'redis',
                'server': ''}
        response = self.client.post(self.test_url, data=data)
        self.assertIn('<h1>Flask-And-Redis test project</h1>', response.data)

        self.assertIn('<h2>Scenario successfully executed</h2>', response.data)
        self.assertIn('&gt; redis.ping()', response.data)
        self.assertIn('True', response.data)
        self.assertIn('&gt; redis.info()', response.data)

    def test_test_default(self):
        data = {'scenario': SCENARIO, 'scenario_type': 'redis', 'server': ''}
        response = self.client.post(self.test_url, data=data)
        self.assertIn('<h2>Scenario successfully executed</h2>', response.data)

    def test_test_errors(self):
        response = self.client.post(self.test_url, data={})
        self.assertIn('<h1>Flask-And-Redis test project</h1>', response.data)

        self.assertIn('>Error</h2>', response.data)
        self.assertIn(
            'One of required fields is not set. Please, check POST request '
            'or try again later.',
            response.data
        )

        data = {'scenario': 'pong', 'scenario_type': 'redis', 'server': ''}
        response = self.client.post(self.test_url, data=data)

        self.assertIn('>Error</h2>', response.data)
        self.assertIn(
            'Cannot convert redis scenario to Python, error is: ',
            response.data
        )

        data = {'scenario': 'redis.pong()',
                'scenario_type': 'python',
                'server': ''}
        response = self.client.post(self.test_url, data=data)

        self.assertIn('>Error</h2>', response.data)
        self.assertIn(
            'Error while executing Python scenario, error is: ',
            response.data
        )

    def test_test_redirect(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response._status_code, 302)
        self.assertEqual(response.location, self.url('home', _external=True))

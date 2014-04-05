"""
====================
testapp.tests.common
====================

Common test case class for tests.

"""

try:
    from unittest2 import TestCase as UnitTestCase
except ImportError:
    from unittest import TestCase as UnitTestCase

from flask.ext.testing import TestCase as BaseTestCase


class TestCase(BaseTestCase, UnitTestCase):

    TESTING = True

    def create_app(self):
        from app import app

        for attr in dir(self):
            if not attr.startswith('_') or attr.isupper():
                continue
            setattr(self, 'old_{0}'.format(attr), app.config.get(attr))
            app.config[attr] = getattr(self, attr)

        return app

    def _post_teardown(self):
        for attr in dir(self):
            if not attr.startswith('old_'):
                continue
            name = attr[4:]
            self.app.config[name] = getattr(self, attr)
        super(TestCase, self)._post_teardown()

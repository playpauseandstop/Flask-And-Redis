"""
==============
testapp.compat
==============

Additional compatibility helpers to work on both of Python 3 and 2.

"""

from flask_redis import IS_PY3


iteritems = lambda data: data.items() if IS_PY3 else data.iteritems()
iterkeys = lambda data: data.keys() if IS_PY3 else data.iterkeys()

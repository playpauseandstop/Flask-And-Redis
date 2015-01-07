"""
=============
testapp.utils
=============

Utilities and helpers for Comments app.

"""

import hashlib
import uuid

from flask import redirect, url_for


to_index = lambda: redirect(url_for('index'))
to_threads = lambda: redirect(url_for('threads'))
uid = lambda: hashlib.sha1(uuid.uuid4().bytes).hexdigest()[:16]

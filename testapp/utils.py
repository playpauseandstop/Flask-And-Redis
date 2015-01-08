"""
=============
testapp.utils
=============

Utilities and helpers for Comments app.

"""

import hashlib
import uuid

from flask import current_app, redirect, url_for


build_key = lambda key, *args, **kwargs: (
    key.format(current_app.config['KEY_PREFIX'], *args, **kwargs)
)
to_index = lambda: redirect(url_for('index'))
to_threads = lambda: redirect(url_for('threads'))
uid = lambda: hashlib.sha1(uuid.uuid4().bytes).hexdigest()[:16]

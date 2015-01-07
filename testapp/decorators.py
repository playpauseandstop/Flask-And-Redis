"""
==================
testapp.decorators
==================

Decorators for Comments app.

"""

from functools import wraps

from flask import g

from utils import to_index


def username_required(func):
    """
    Make sure that username stored in session, before executing actual view
    function.

    :param func: View function to decorate.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        r"""
        Run view function if session contains username, otherwise redirect to
        index page.

        :param \*args: Positional arguments to pass to view function.
        :param \*\*kwargs: Keyword arguments to pass to view function.
        """
        if not g.username:
            return to_index()
        return func(*args, **kwargs)
    return wrapper

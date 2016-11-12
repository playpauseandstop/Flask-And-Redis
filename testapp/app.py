"""
===========
testapp.app
===========

Implement Flask app for Comments app and provide abilit to run development
server.

"""

from __future__ import print_function

import datetime
import os
import sys

from flask import Flask, g, session
from flask_lazyviews import LazyViews
from flask_redis import Redis

import constants
import settings

from compat import iteritems


def create_app(**options):
    r"""Factory function to create test application.

    :param \*\*options: Override default settings from given options.
    :type \*\*options: dict
    """
    # Initialize application and configure it from settings and given options
    app = Flask('testapp')
    app.config.from_object(settings)
    app.config.update(options)

    # Put necessary filter & globals to Jinja environment
    app.jinja_env.filters['format'] = format
    app.jinja_env.globals['constants'] = constants
    app.jinja_env.globals.update({
        'constants': constants,
        'float': float,
        'fromtimestamp': datetime.datetime.fromtimestamp,
        'iteritems': iteritems,
        'len': len,
    })

    # Register Redis databases
    Redis(app, 'REDIS_LINKS')
    Redis(app, 'REDIS_CONTENT')

    # Setup all available routes
    views = LazyViews(app, 'views')
    views.add('/', 'index', methods=('GET', 'POST'))
    views.add('/comments/<thread_uid>', 'comment', methods=('POST', ))
    views.add('/comments/<thread_uid>', 'comments')
    views.add('/quit', 'quit')
    views.add('/threads', 'start_thread', methods=('POST', ))
    views.add('/threads', 'threads')
    views.add('/threads/<thread_uid>/delete',
              'delete_thread',
              methods=('GET', 'POST'))
    views.add_error(400, 'error')
    views.add_error(403, 'error')
    views.add_error(404, 'error')
    views.add_error(Exception, 'error')

    # Put username from session to globals before each request
    @app.before_request
    def global_username():
        key = constants.USERNAME_KEY.format(app.config['KEY_PREFIX'])
        g.username = session.get(key) or ''

    return app


def main():
    """Run test server for Comments app."""
    counter = len(sys.argv)
    host, port = constants.SERVER_HOST, constants.SERVER_PORT

    if counter == 2:
        mixed = sys.argv[1]
        if ':' in mixed:
            host, port = mixed.split(':')
        else:
            port = mixed

        try:
            port = int(port)
        except (TypeError, ValueError):
            return usage()
    elif counter > 2:
        return usage()

    try:
        debug = int(os.environ.get('FLASK_DEBUG'))
    except (TypeError, ValueError):
        debug = None

    return app.run(host, port, debug=debug)


def usage():
    """Print simple usage note."""
    print('Usage: {0} HOST:PORT'.format(os.path.basename(sys.argv[0])),
          file=sys.stderr)
    return True


#: Global Comments app instance
app = create_app()


if __name__ == '__main__':
    sys.exit(int(main()))

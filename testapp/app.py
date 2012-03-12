#!/usr/bin/env python

import os
import sys

from flask import Flask, redirect, url_for
from flask.ext.redis import Redis

import settings


# Initialize simple Flask application
app = Flask(__name__)
app.config.from_object(settings)

# Setup Redis conection
redis = Redis(app)


# Add two simple views: One for forgetting counter
@app.route('/forget-us')
def forget_us():
    key = app.config['COUNTER_KEY']
    redis.delete(key)
    return redirect(url_for('home'))


# Second for remembering visiting counter
@app.route('/')
def home():
    key = app.config['COUNTER_KEY']
    counter = redis.incr(key)
    message = 'Hello, visitor!'

    if counter != 1:
        message += "\nThis page viewed %d time(s)." % counter

    return message


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000

    if len(sys.argv) == 2:
        mixed = sys.argv[1]

        try:
            host, port = mixed.split(':')
        except ValueError:
            port = mixed
    elif len(sys.argv) == 3:
        host, port = sys.argv[1:]

    try:
        port = int(port)
    except (TypeError, ValueError):
        print >> sys.stderr, 'Please, use proper digit value to the ' \
                             '``port`` argument.\nCannot convert %r to ' \
                             'integer.' % port

    app.debug = bool(int(os.environ.get('DEBUG', 1)))
    app.run(host=host, port=port)

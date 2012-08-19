#!/usr/bin/env python

import os
import sys

from flask import Flask, redirect, render_template, request, url_for
from flask.ext.redis import Redis

import settings

from scenarios.default import SCENARIO, convert_scenario
from scenarios.run import run_scenario


# Initialize simple Flask application
app = Flask(__name__)
app.config.from_object(settings)

# Setup Redis conection
redis = Redis(app)


@app.route('/')
def home():
    """
    Show basic information about server and add form to test server.
    """
    context = {
        'info': redis.info(),
        'scenario_python': convert_scenario(SCENARIO),
        'scenario_redis': SCENARIO,
    }

    return render_template('index.html', **context)


@app.route('/test', methods=('GET', 'POST'))
def test():
    """
    Test Redis server, using scenario from POST request.
    """
    if request.method == 'GET':
        return redirect(url_for('home'))

    scenario_type = request.form.get('scenario_type')
    scenario = request.form.get('scenario')

    if not scenario or not scenario_type:
        return render_template('test.html', error='required_field')

    if scenario_type == 'redis':
        try:
            scenario = convert_scenario(scenario)
        except ValueError as e:
            return render_template('test.html', error='convert', exception=e)

    try:
        results = run_scenario(redis, scenario)
    except Exception as e:
        return render_template('test.html', error='exception', exception=e)

    context = {
        'results': results,
        'scenario': scenario,
        'scenario_type': scenario_type,
    }

    return render_template('test.html', **context)


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

import os
import sys
import traceback

from flask import Flask, redirect, render_template, request, url_for
from flask.ext.redis import Redis
from flask.ext.script import Manager

import settings

from scenarios.default import SCENARIO, convert_scenario
from scenarios.run import run_scenario


# Initialize simple Flask application
app = Flask(__name__)
app.config.from_object(settings)

# Initialize script extension
manager = Manager(app)

# Setup Redis conection or connections with multiple services
redis = Redis(app)
redis_backup = Redis()
redis_slave = Redis()


@app.before_first_request
def init_multiple_redis():
    """
    Initialize multiple redis instances if necessary.
    """
    if app.config['MULTIPLE_REDIS_SERVERS']:
        redis_backup.init_app(app, 'REDIS_BACKUP')
        redis_slave.init_app(app, 'REDIS_SLAVE')


@app.route('/')
def home():
    """
    Show basic information about server and add form to test server.
    """
    instance = redis_instance(request.args.get('server', ''))

    context = {
        'info': instance.info(),
        'scenario_python': convert_scenario(SCENARIO),
        'scenario_redis': SCENARIO,
        'server': instance.server,
    }

    return render_template('index.html', **context)


def redis_instance(server):
    """
    Return redis instance by server suffix.
    """
    key = 'redis_{0}'.format(server) if server else 'redis'
    instance = globals()[key]
    instance.server = server
    return instance


@app.route('/test', methods=('GET', 'POST'))
def test():
    """
    Test Redis server, using scenario from POST request.
    """
    if request.method == 'GET':
        return redirect(url_for('home'))

    instance = redis_instance(request.form.get('server', ''))
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
        results = run_scenario(instance, scenario)
    except Exception as e:
        kwargs = {'error': 'exception',
                  'exception': e,
                  'traceback': traceback.format_exc()}
        return render_template('test.html', **kwargs)

    context = {
        'results': results,
        'scenario': scenario,
        'scenario_type': scenario_type,
        'server': instance.server,
    }

    return render_template('test.html', **context)

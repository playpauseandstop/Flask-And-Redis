"""
=====================
testapp.scenarios.run
=====================

Run Python scenario in secured Sandbox.

"""

import time

from flask.ext.redis import Redis
from sandbox import Sandbox, proxy


__all__ = ('run_scenario', )


proxy.SAFE_TYPES = tuple(list(proxy.SAFE_TYPES) + [type(Redis()), set])


def run_scenario(redis, scenario):
    """
    Run Python scenario with ``redis`` instance.
    """
    data = {'redis': redis}
    results = []
    sandbox = Sandbox()
    start = time.time()

    for raw in scenario.splitlines():
        line = 'result = {0}'.format(raw) if '=' not in raw else raw
        sandbox.execute(line, {}, data)
        results.append((raw, data['result'] if 'result' in data else None))

    return {'results': results, 'time': time.time() - start}

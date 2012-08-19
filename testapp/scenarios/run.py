import time


__all__ = ('run_scenario', )


def run_scenario(redis, scenario):
    """
    Run Python scenario with ``redis`` instance.
    """
    results = []
    start = time.time()

    for line in scenario.splitlines():
        result = eval(line)
        results.append((line, result))

    return {'results': results, 'time': time.time() - start}

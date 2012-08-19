import os

from decimal import ROUND_UP, Decimal

import redis


__all__ = ('SCENARIO', 'convert_scenario')


DIRNAME = os.path.abspath(os.path.dirname(__file__))
SCENARIO = open(os.path.join(DIRNAME, 'scenario.redis'), 'rb').read()


def convert_scenario(scenario):
    """
    Convert redis scenario to python.
    """
    def convert_hmset_args(args):
        name = args[0]
        args = args[1:]
        data = {}
        for i, arg in enumerate(args):
            if i % 2 == 1:
                continue
            data[arg] = args[i + 1]
        return name, data

    def convert_zadd_args(args):
        result = [args[0]]
        for i, arg in enumerate(args[1:]):
            if i % 2 == 1:
                continue
            result.append(args[i + 2])
            result.append(arg)
        return result

    convert_args = {
        'hmget': lambda args: [args[0], args[1:]],
        'hmset': convert_hmset_args,
        'zadd': convert_zadd_args,
    }
    convert_cmds = {
        'del': 'delete',
        'incrby': 'incr',
    }
    result = []

    if redis.__version__.startswith('2.4'):
        convert_args.update({'getrange': lambda args: ['getrange'] + args})
        convert_cmds.update({'getrange': 'execute_command'})

    for line in scenario.splitlines():
        arg, args, ignore_whitespace = '', [], False

        try:
            cmd, raw_args = line.split(' ', 1)
        except ValueError:
            cmd, raw_args = line, ''

        cmd = cmd.lower()
        raw_cmd = cmd

        if cmd in convert_cmds:
            cmd = convert_cmds[cmd]

        if not hasattr(redis.Redis, cmd):
            raise ValueError('Cannot find {0!r} redis command.'.format(cmd))

        for i, raw in enumerate(raw_args):
            if raw == ' ':
                if not ignore_whitespace:
                    args.append(arg)
                    arg = ''
                    continue

            if raw == '"':
                ignore_whitespace = True

            arg += raw

            if i == len(raw_args) - 1:
                args.append(arg)

        if cmd in convert_args:
            args = convert_args[cmd](args)
        elif raw_cmd in convert_args:
            args = convert_args[raw_cmd](args)

        args = list(args)

        for i, arg in enumerate(args):
            if not isinstance(arg, basestring):
                args[i] = str(arg)
            elif arg.isdigit():
                continue
            else:
                args[i] = "{0!r}".format(arg.strip('"'))

        result.append('redis.{0}({1})'.format(cmd, ', '.join(args)))

    return '\n'.join(result)

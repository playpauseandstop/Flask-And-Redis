#!/usr/bin/env python
"""
Bootstrap project using virtualenv_ and pip_. This script will create new
virtual environment if needed and will install all requirements there.

.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _pip: http://pypi.python.org/pypi/pip

"""

import ConfigParser
import copy
import os
import shutil
import sys

from distutils.core import run_setup


try:
    import pip
except ImportError, e:
    print('ERROR: %s') % e
    print('ERROR: This script requires pip installed in your system.')
    sys.exit(1)


try:
    import virtualenv
except ImportError, e:
    print('ERROR: %s') % e
    print('ERROR: This script requires virtualenv installed in your system.')
    sys.exit(1)


# Default configuration for bootstrap script. You may override configuration
# in ``bootstrap.cfg`` file.
CONFIG = {
    'pip': {
        'download_cache': '%(DEST_DIR)s/src',
        'requirements': 'requirements.txt',
        'quiet': False,
        'upgrade': False,
        'verbose': False,
    },
    'virtualenv': {
        'clear': False,
        'dest_dir': 'env',
        'quiet': 0,
        'site_packages': False,
        'unzip_setuptools': True,
        'verbose': 0,
    },
}
DIRNAME = os.path.abspath(os.path.dirname(__file__))


def create_environment():
    dest_dir = os.path.join(DIRNAME, CONFIG['virtualenv']['dest_dir'])
    dest_dir = os.path.abspath(dest_dir)

    # Create new virtual environment
    print('Step 1. Create new virtual environment')

    if not os.path.isdir(dest_dir) or CONFIG['virtualenv']['clear']:
        kwargs = copy.copy(CONFIG['virtualenv'])
        kwargs['home_dir'] = kwargs['dest_dir']

        verbosity = int(kwargs['verbose']) - int(kwargs['quiet'])
        logger = virtualenv.Logger([
            (virtualenv.Logger.level_for_integer(2 - verbosity), sys.stdout),
        ])

        del kwargs['dest_dir'], kwargs['quiet'], kwargs['verbose']

        virtualenv.logger = logger
        virtualenv.create_environment(**kwargs)
    else:
        print('Virtual environment %r already exists.' % \
              CONFIG['virtualenv']['dest_dir'])


def install_requirements():
    print('\nStep 2. Install requirements')

    # Install requirements from ``requirements.txt`` file
    requirements_file = os.path.join(DIRNAME, CONFIG['pip']['requirements'])

    if os.path.isfile(requirements_file):
        args = ['install',
                '-E', CONFIG['virtualenv']['dest_dir'],
                '-r', CONFIG['pip']['requirements']]

        if CONFIG['pip']['download_cache']:
            download_cache = \
                CONFIG['pip']['download_cache'] % template_context()
            args.extend(['--download-cache', download_cache])

        for name in ('quiet', 'upgrade', 'verbose'):
            if CONFIG['pip'][name]:
                args.append('--' + name)

        try:
            pip.main(args)
        except SystemExit, e:
            if e.code:
                raise e
    else:
        print('ERROR: Cannot to find requirements file at %r.' % \
              requirements_file)
        sys.exit(1)


def main():
    """
    Create new virtualenv and install all pip requirements there.
    """
    # Change directory to current
    os.chdir(DIRNAME)

    # Read configuration values from ``bootstrap.cfg`` file if possible
    read_config('bootstrap.cfg')

    # Parse destination directory for new virtual environment
    create_environment()

    # Install all requirements to this virtual environment if possible
    install_requirements()


def read_config(config_file):
    global CONFIG

    if not config_file.startswith(DIRNAME):
        config_file = os.path.abspath(os.path.join(DIRNAME, config_file))

    if not os.path.isfile(config_file):
        return

    config = ConfigParser.ConfigParser()
    config.read(config_file)

    print('Load bootstrap configuration from %r.' % config_file)

    for section in ('pip', 'virtualenv'):
        try:
            items = config.items(section)
        except ConfigParser.NoSectionError:
            continue

        for key in CONFIG[section].keys():
            if key in items:
                CONFIG[section][key] = items[key]


def template_context():
    return {'DEST_DIR': CONFIG['virtualenv']['dest_dir']}


if __name__ == '__main__':
    main()

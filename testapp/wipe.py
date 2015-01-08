"""
============
testapp.wipe
============

Wipe all data from Links and Content storages.

"""

import sys
import time

from app import app
from compat import iteritems
from constants import THREADS_KEY
from utils import build_key


def main():
    """Wipe all data from Links and Content storages."""
    start_time = time.time()
    print('Start deleting available Threads')

    with app.app_context():
        # Storage requires app in global context
        import storage

        for thread_uid, thread in iteritems(storage.list_threads()):
            storage.delete_thread(thread_uid)
            print('    Thread deleted! UID #{0}, subject: {1}'.
                  format(thread_uid, thread['subject']))

        storage.links.delete(build_key(THREADS_KEY))

    print('All Threads deleted. Done in {0:.4f}s'.
          format(time.time() - start_time))
    return False


if __name__ == '__main__':
    sys.exit(int(main()))

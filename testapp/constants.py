"""
=================
testapp.constants
=================

Constants to use in Comments app.

"""

# Server constants
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8300

# Error messages
ERRORS = {
    'comment': {
        'text': 'Invalid value for comment text.',
    },
    'delete_thread': {
        'confirm': 'Cannot confirm deleting thread.',
    },
    'start_thread': {
        'subject': 'Invalid value for thread subject.',
    },
}

# Redis keys
COMMENT_KEY = '{0}:thread:{1}:{2}'
THREAD_KEY = '{0}:thread:{1}'
THREAD_COMMENTS_KEY = '{0}:thread:{1}:comments'
THREAD_COUNTER_KEY = '{0}:thread:{1}:counter'
THREADS_KEY = '{0}:threads'

# Session keys
USERNAME_KEY = '{0}:username'

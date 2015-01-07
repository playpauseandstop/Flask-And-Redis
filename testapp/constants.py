"""
=================
testapp.constants
=================

Constants to use in Comments app.

"""

# Server constants
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8300

# Redis keys
COMMENT_KEY = '{0}:thread:{1}:{2}'
THREAD_KEY = '{0}:thread:{1}'
THREAD_COMMENTS_KEY = '{0}:thread:{1}:comments'
THREAD_COUNTER_KEY = '{0}:thread:{1}:counter'
THREADS_KEY = '{0}:threads'

# Session keys
USERNAME_KEY = '{0}:username'

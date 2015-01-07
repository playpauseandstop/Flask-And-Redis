"""
================
testapp.settings
================

Settings for Comments app.

"""

# Flask settings
DEBUG = False
SECRET_KEY = 'Please, setup proper secret key in local settings.'

# Links database
REDIS_LINKS_DECODE_RESPONSES = True
REDIS_LINKS_URL = 'redis://127.0.0.1:6379/0'

# Content database
REDIS_CONTENT_DECODE_RESPONSES = True
REDIS_CONTENT_URL = 'redis://127.0.0.1:6379/1'

# Comments app settings
KEY_PREFIX = 'far_testapp'
THREADS_PER_PAGE = 15


# Import local settings
try:
    import settings_local
except ImportError:
    pass
else:
    for attr in dir(settings_local):
        if attr.startswith('_') or not attr.isupper():
            continue
        locals()[attr] = getattr(settings_local, attr)
    del settings_local

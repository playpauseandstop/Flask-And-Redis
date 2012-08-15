COUNTER_KEY = 'testapp:counter'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0


try:
    import settings_local
except ImportError:
    pass
else:
    for attr in dir(settings_local):
        if attr.startswith('_'):
            continue
        locals()[attr] = getattr(settings_local, attr)

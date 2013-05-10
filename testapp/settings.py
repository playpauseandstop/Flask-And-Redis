import redis

# Check redis version
IS_24 = redis.__version__.startswith('2.4')


# Redis settings
REDIS_CLASS = 'redis.Redis' if IS_24 else 'redis.StrictRedis'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

REDIS_BACKUP_HOST = 'localhost'
REDIS_BACKUP_PORT = 6380
REDIS_BACKUP_DB = 0

REDIS_SLAVE_HOST = 'localhost'
REDIS_SLAVE_PORT = 6381
REDIS_SLAVE_DB = 0

# Enable multiple redis servers and showing traceback on errors, by default not
MULTIPLE_REDIS_SERVERS = False
SHOW_TRACEBACK = False


try:
    import settings_local
except ImportError:
    pass
else:
    for attr in dir(settings_local):
        if attr.startswith('_'):
            continue
        locals()[attr] = getattr(settings_local, attr)

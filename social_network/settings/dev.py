from social_network.settings.common import *

DEBUG = True

INSTALLED_APPS += ['debug_toolbar']


DATABASES = {
    'default': {
        'PORT': '5430',
        'NAME': 'social_network',
        'USER': 'postgres',
        'CONN_MAX_AGE': 0,
        'CONN_HEALTH_CHECKS': True,
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'ENGINE': 'django.db.backends.postgresql',
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "TIMEOUT": 300,
        },
    }
}


REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += ['rest_framework.renderers.BrowsableAPIRenderer']

MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")

CORS_ALLOW_ALL_ORIGINS = True

INTERNAL_IPS = [
    "127.0.0.1",
]

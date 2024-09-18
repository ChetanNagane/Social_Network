from social_network.settings.common import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'social_network',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'postgres',
        'PORT': '5432',
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",  # Use Redis service name
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "TIMEOUT": 300,
        },
    }
}


CORS_ALLOW_ALL_ORIGINS = True

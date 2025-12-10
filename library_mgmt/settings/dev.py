from .base import *

# Debug mode
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = []

# Allowed origins
CORS_ALLOWED_ORIGINS = []

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

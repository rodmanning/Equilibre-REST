"""Custom config for 'demo' deployment of API."""

import os
import datetime

from corsheaders.defaults import default_headers

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SomeSuperSecretStringThatYouNeedToKeepSafe!'

# SECURITY WARNING: keep the allowed hosts limited to just those required
ALLOWED_HOSTS = []

# SECURITY WARNING: CORS Headers Settings
# Production setting should whitelist allowed hosts
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     'localhost:8080',
#     '127.0.0.1:9080',
#     '192.168.178.31:8000', # Trish home network
# )

CORS_ALLOW_HEADERS = default_headers + (
    'access-control-allow-origin',
    'access-control-expose-headers',
)

# WSGI script
WSGI_APPLICATION = 'equilibre.wsgi.application'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Datebase config
DATABASES = {
    'default': {
        'Details go here ...'
    }
}

ADMINS = (
    ('Rod Manning', 'rod.t.manning@gmail.com')
)
MANAGERS = ADMINS

# URL for serving static files
STATIC_URL = '/static/'

# Set the STATIC_ROOT to the path on the server where the static files are to
# be served from.
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_root')

# URL for serving media files
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    # Authentication
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    # Filtering
    #"DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
}

import os

import dj_database_url

from .common import *

DEBUG = True

SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = ["teladoshi.com",".teladoshi.com","localhost","127.0.0.1","[::1]",".railway.internal"]
CSRF_TRUSTED_ORIGINS = ["https://teladoshi.com","https://*.teladoshi.com"]
CSRF_COOKIE_DOMAIN = ".teladoshi.com"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_DOMAIN = ".teladoshi.com"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


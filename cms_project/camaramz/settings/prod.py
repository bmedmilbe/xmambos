import os



from .common import *

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'teladoshi.com',
    '*.teladoshi.com',
    '*.railway.internal',
    'gateway.railway.internal',
    'cms.railway.internal',
]
CSRF_TRUSTED_ORIGINS = ["https://teladoshi.com","https://*.teladoshi.com"]
CSRF_COOKIE_DOMAIN = ".teladoshi.com"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_DOMAIN = ".teladoshi.com"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


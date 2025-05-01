from .base import *
import environ
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)

def parse_env_list(var_name):
    return [item.strip() for item in get_env_variable(var_name).split(',') if item.strip()]

SECRET_KEY = get_env_variable('DJANGO_SECRET')
DEBUG = get_env_variable('DJANGO_DEBUG') == 'True'

# 배포
ALLOWED_HOSTS = parse_env_list('DJANGO_ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = parse_env_list('DJANGO_CSRF_TRUSTED_ORIGINS')
CORS_ALLOWED_ORIGINS = parse_env_list('DJANGO_CORS_ALLOWED_ORIGINS')

DBNAME = get_env_variable('DBNAME')
DBUSER = get_env_variable('DBUSER')
DBPASSWORD = get_env_variable('DBPASSWORD')
DBHOST = get_env_variable('DBHOST')
DBPORT = get_env_variable('DBPORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DBNAME,
        'USER': DBUSER,
        'PASSWORD': DBPASSWORD, 
        'HOST': DBHOST, 
        'PORT': DBPORT,
        'CHARSET': 'utf8mb4',
        'COLLATION': 'utf8mb4_unicode_ci',
    }
}
from .base import *
import environ

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_env_variable('DJANGO_SECRET')

# 배포
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".cloudtype.app"]
CSRF_TRUSTED_ORIGINS = ['https://*.cloudtype.app']


DEBUG = True

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
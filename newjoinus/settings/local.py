from .base import *
import environ

# 환경 변수 설정
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))  # .env 파일 읽기

SECRET_KEY = env('DJANGO_SECRET')

ALLOWED_HOSTS = ['*']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
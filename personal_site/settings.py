"""
Django settings for personal_site project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import configparser
import os

from pathlib import Path
from dotenv import load_dotenv

# load_dotenv()

# configParser = configparser.ConfigParser()
# configParser.read('config.ini')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '')
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(' ')
# APPEND_SLASH=False

# ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "freedom_of_speech.apps.FreedomOfSpeechConfig",
    "portfolio.apps.PortfolioConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SAMESITE = 'Strict'
# SESSION_COOKIE_SAMESITE = 'Strict'
# DCS_SESSION_COOKIE_SAMESITE = 'None'

# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# CSRF_TRUSTED_ORIGINS = ['https://127.0.0.1:80']

ROOT_URLCONF = "personal_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / 'templates',
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "personal_site.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    #"default": {
    #    "ENGINE": "django.db.backends.sqlite3",
    #    "NAME": BASE_DIR / "db.sqlite3",
    #}
    # 'default': {
    #    'ENGINE': 'djongo',
    #    'NAME': 's1te',
    #    'ENFORCE_SCHEMA': False,
    #    'CLIENT': {
    #        'host': "mongodb+srv://%s:%s@%s" % (quote_plus(configParser['mongodb']['MONGODATABASE_USER']),
    #                                            quote_plus(configParser['mongodb']['MONGODATABASE_PASSWORD']),
    #                                            configParser['mongodb']['MONGODATABASE_HOST'])
    #    },
    # }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'
#MEDIA_URL = '/img/'

STATICFILES_DIRS = [
    BASE_DIR / 'freedom_of_speech/static',
    BASE_DIR / 'portfolio/static',
]

#MEDIA_ROOT = BASE_DIR / 'static/assets/img'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(os.path.join(PROJECT_ROOT, 's1te'))

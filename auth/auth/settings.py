"""
Django settings for auth project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import json
import pymongo

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-h$xzz_o32@=@gjwl##_v&(@-1kn68(em^56h7r86@$9)6_!qa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Key file path

DATABASE_SETTINGS_FILE = os.path.join(os.path.join(BASE_DIR, 'keys'), 'db_settings.json')
GOOGLE_API_SETTINGS_FILE = os.path.join(os.path.join(BASE_DIR, 'keys'), 'googleapi.json')
KAKAO_API_SETTINGS_FILE = os.path.join(os.path.join(BASE_DIR, 'keys'), 'kakaoapi.json')
NAVER_API_SETTINGS_FILE = os.path.join(os.path.join(BASE_DIR, 'keys'), 'naverapi.json')
NETWORK_SETTINGS_FILE = os.path.join(os.path.join(BASE_DIR, 'keys'), 'networks.json')

# Network Address

network_info = json.loads(open(NETWORK_SETTINGS_FILE).read())
BASE_URL = network_info['base']
FRONT_SERVER = network_info['frontServer']
API_SERVER = network_info['apiServer']
AUTH_SERVER = network_info['authServer']
DB_SERVER = network_info['dbServer']

ALLOWED_HOSTS = [
    BASE_URL['URN']
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'auth.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'auth.wsgi.application'

# Database

db_info = json.loads(open(DATABASE_SETTINGS_FILE).read())
DB_DATABASE = db_info['Accounts']['database']
DB_HOST = db_info['Accounts']['host']
DB_USERNAME = db_info['Accounts']['username']
DB_PASSWORD = db_info['Accounts']['password']

pymongo.mongo_client.MongoClient.HOST = DB_HOST
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': DB_DATABASE,
        'CLIENT': {
            'host': DB_HOST,
            'username': DB_USERNAME,
            'password': DB_PASSWORD,
            'authMechanism': 'SCRAM-SHA-1'
        },
        'LOGGING': {
            'version': 1,
            'loggers': {
                'djongo': {
                    'level': 'DEBUG',
                    'propagate': False,                        
                }
            },
        },
    }
}

# Google API Setting

google_api_info = json.loads(open(GOOGLE_API_SETTINGS_FILE).read())
GOOGLE_AUTH_SCOPES = google_api_info['GOOGLE_AUTH_SCOPES']
GOOGLE_REDIRECT_URI = google_api_info['web']['redirect_uris'][0]

# Kakao API Setting

kakao_api_info = json.loads(open(KAKAO_API_SETTINGS_FILE).read())
KAKAO_NATIVE_APP_KEY = kakao_api_info['native_app_key']
KAKAO_REST_API_KEY = kakao_api_info["rest_api_key"]
KAKAO_JAVASCRIPT_KEY = kakao_api_info["javascript_key"]
KAKAO_ADMIN_KEY = kakao_api_info["admin_key"]
KAKAO_CLIENT_SECRET = kakao_api_info["client_secret"]
KAKAO_REDIRECT_URI = kakao_api_info["redirect_uris"][0]

# Naver API Setting

naver_api_info = json.loads(open(NAVER_API_SETTINGS_FILE).read())
NAVER_CLIENT_ID = naver_api_info['client_id']
NAVER_CLIENT_SECRET = naver_api_info['client_secret']
NAVER_REDIRECT_URI = naver_api_info['redirect_uris'][0]

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

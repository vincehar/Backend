"""
Django settings for NHPartners project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import mongoengine



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1fqjjpf=2y_qo0cmehc1_f_5--z&g58&&jm=wsmx!6j3uusc(3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# MongoDB settings
#MONGODB_DATABASES = {
#    'default': {'name': 'django_mongoengine'}
#}
#DJANGO_MONGOENGINE_OVERRIDE_ADMIN = True
#
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy'
    }
}

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'upto',
    #'mongo_auth',
    #'mongo_auth.contrib',
    'sekizai',
    'mongoengine',
    'django_browserid',
    'mongoengine.django.mongo_auth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'mongo_auth.middleware.LazyUserMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)



AUTHENTICATION_BACKENDS = (
    'django_mongoengine.mongo_auth.backends.MongoEngineBackend',
    'mongoengine.django.auth.MongoEngineBackend',
    #'mongo_auth.backends.MongoEngineBackend',
    #'mongo_auth.backends.FacebookBackend',
    #'mongo_auth.backends.TwitterBackend',
    #'mongo_auth.backends.FoursquareBackend',
    #'mongo_auth.backends.GoogleBackend',
    #'mongo_auth.backends.BrowserIDBackend',
    #'mongo_auth.backends.LazyUserBackend',
)

ROOT_URLCONF = 'NHPartners.urls'

WSGI_APPLICATION = 'NHPartners.wsgi.application'

#USER_CLASS = 'mongo_auth.contrib.models.User'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


AUTH_USER_MODEL = 'mongo_auth.MongoUser'
MONGOENGINE_USER_DOCUMENT = 'mongoengine.django.auth.User'
SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'
mongoengine.connect('upto', host='mongodb://localhost/upto')

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS_DIRS': True,
        'DIRS': [
            os.path.join(os.path.realpath(os.path.dirname(__file__)), '../templates')
        ],

        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                #'mongo_auth.contrib.context_processors.mongo_auth',
                #'sekizai.context_processors.sekizai',
            ],
            'debug' : [True]
        },
    },
]

STATIC_URL = '/static/'


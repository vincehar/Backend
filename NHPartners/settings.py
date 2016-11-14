"""
Django settings for NHPartners project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import django
import mongoengine
from pymongo.read_preferences import ReadPreference

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1fqjjpf=2y_qo0cmehc1_f_5--z&g58&&jm=wsmx!6j3uusc(3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    'http://127.0.0.1:8000',
]

CORS_ORIGIN_ALLOW_ALL = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# MongoDB settings
# MONGODB_DATABASES = {
#    'default': {'name': 'django_mongoengine'}
# }
# DJANGO_MONGOENGINE_OVERRIDE_ADMIN = True
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
    #'social_auth',
    # 'mongo_auth',
    # 'mongo_auth.contrib',
    #'sekizai',
    'mongoengine',
    #'django_browserid',
    'mongoengine.django.mongo_auth',
    'rest_framework',
    'rest_framework_mongoengine',
    'corsheaders',
    'regme',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'mongo_auth.middleware.LazyUserMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    # 'django_mongoengine.mongo_auth.backends.MongoEngineBackend',
    'mongoengine.django.auth.MongoEngineBackend',
    #'social_auth.backends.twitter.TwitterBackend',
    #'social_auth.backends.facebook.FacebookBackend',
    #'social_auth.backends.google.GoogleOAuthBackend',
    #'social_auth.backends.google.GoogleOAuth2Backend',
    #'social_auth.backends.google.GoogleBackend',
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    ),
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

ROOT_URLCONF = 'NHPartners.urls'

WSGI_APPLICATION = 'NHPartners.wsgi.application'

CORS_ALLOW_CREDENTIALS = True

# USER_CLASS = 'mongo_auth.contrib.models.User'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

AUTHENTICATION_BACKENDS = (
           'mongoengine.django.auth.MongoEngineBackend',
 )
AUTH_USER_MODEL = 'mongo_auth.MongoUser'
MONGOENGINE_USER_DOCUMENT = 'mongoengine.django.auth.User'
#MONGOENGINE_USER_DOCUMENT = 'regme.documents.User'
SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'
mongoengine.connect(os.environ.get('DATABASE_NAME'), host='mongodb://'+os.environ.get('DATABASE_URL') + '/' + os.environ.get('DATABASE_NAME'), read_preference=ReadPreference.PRIMARY)

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
        # 'DIRS_DIRS': True,
        'DIRS': [
            os.path.join(os.path.realpath(os.path.dirname(__file__)), '../upto/templates')
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
                # 'mongo_auth.contrib.context_processors.mongo_auth',
                # 'sekizai.context_processors.sekizai',
            ],
            'debug': [True]
        },
    },
]

STATIC_URL = '/static/'

# Facebook
FACEBOOK_APP_ID = '222535738090638'
FACEBOOK_API_SECRET = '09a2f8b2122cd05061e50fa00dcc999a'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
django.setup()
#SOCIAL_AUTH_MODELS = 'social_auth.db.mongoengine_models'
#SOCIAL_AUTH_USER_MODEL = 'mongoengine.django.auth.User'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/upto/wishes/'
LOGIN_ERROR_URL = '/login-error/'

#SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
#SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

ACCOUNT_ACTIVATION_DAYS = 2

SITE = {'domain': '127.0.0.1:8000', 'name': 'YouWeesh'}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'alexandre.frigout@gmail.com'
EMAIL_HOST_PASSWORD = 'njgjxbwgwucqypdf'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

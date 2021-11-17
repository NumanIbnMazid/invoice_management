""" # Project Common Settings # """
from pathlib import Path
import os
from dotenv import load_dotenv


""" *** Project Directory Configurations *** """
BASE_DIR = Path(__file__).resolve().parent.parent.parent

""" *** Read Project Environment File *** """
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path)

""" *** Application Secret Key *** """
SECRET_KEY = os.environ.get('SECRET_KEY')

""" *** DEBUG Configurations *** """
if eval(str(os.environ.get('IS_PRODUCTION'))) == True or eval(str(os.environ.get('IS_STAGING'))) == True:
    DEBUG = False
else:
    DEBUG = True
    
""" *** Database URL Configurations *** """
if eval(str(os.environ.get('IS_PRODUCTION'))) and os.environ.get('PRODUCTION_DATABASE_URL'):
    DYNAMIC_DATABASE_URL = os.environ.get('PRODUCTION_DATABASE_URL')
elif eval(str(os.environ.get('IS_STAGING'))) and os.environ.get('STAGING_DATABASE_URL'):
    DYNAMIC_DATABASE_URL = os.environ.get('STAGING_DATABASE_URL')
elif os.environ.get('DEVELOPMENT_DATABASE_URL'):
    DYNAMIC_DATABASE_URL = os.environ.get('DEVELOPMENT_DATABASE_URL')
else:
    DYNAMIC_DATABASE_URL = None


""" *** Application Definitions *** """
THIRD_PARTY_APPS = [
    # Django Debug Toolbar
    "debug_toolbar",
    # Django Crispy Forms
    "crispy_forms",
    # Django Widget Tweaks
    "widget_tweaks",
    # Django Ck Editor
    'ckeditor',
    'ckeditor_uploader',
    # Django Allauth
    'allauth',
    'allauth.account',
    # Django Select2
    "django_select2",
]

LOCAL_APPS = [
    "utils",
    "users",
    "company",
    "service",
    "deals",
    "invoice",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Django WhiteNoise
    "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',
    'django.contrib.sites',
] + THIRD_PARTY_APPS + LOCAL_APPS


""" *** Authentication Definitions *** """
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
]

""" *** Middlewares Definitions *** """
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Django Whitenoise Middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Django Debug Toolbar Middleware
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Request Middleware
    'middlewares.request_middleware.RequestMiddleware',
]

""" *** Template Definitions *** """
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

""" *** Authentication Password Validators *** """
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

""" *** Localization Configuration *** """
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

""" *** Static & Media Files Configurations *** """
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

""" *** Other Definitions *** """
SITE_ID = 1
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
# ASGI_APPLICATION = "config.routing.application"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
HOME_URL = "/"
ADMIN_LOGIN_URL = "/accounts/login"
LOGIN_URL = ADMIN_LOGIN_URL
SITE_DOMAIN="titas.com"

# Crispy Form Configuraton
CRISPY_FAIL_SILENTLY = not DEBUG


""" # Project Third Party Packages Configurations # """
from config.settings.third_party_configs import *
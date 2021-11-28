""" # Production Environment Configurations # """
# import common configurations
from config.settings.common import *
import dj_database_url

""" *** Application Allowed Hosts *** """
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(" ")

""" *** Database Configuration *** """
try:
    if DYNAMIC_DATABASE_URL:
        DATABASE_URL = DYNAMIC_DATABASE_URL
    else:
        try:
            if eval(str(os.environ.get('DOCKER_BUILD'))) == True:
                DATABASE_URL = f"postgres://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
            else:
                DATABASE_URL = f"postgres://{os.environ.get('POSTGRES_DB_USER')}:{os.environ.get('POSTGRES_DB_PASSWORD')}@{os.environ.get('POSTGRES_DB_HOST')}:{os.environ.get('POSTGRES_DB_PORT')}/{os.environ.get('POSTGRES_DB_NAME')}"
        except Exception as e:
            print("*** Exception ***", e)
            DATABASE_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

    # Define DATABASES
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=True)
    }
except Exception as E:
    print("*** Exception ***", E)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ==================== Security Modules ===================
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
X_FRAME_OPTIONS = 'DENY'
# set low, but when site is ready for deployment, set to at least 15768000 (6 months)
SECURE_HSTS_SECONDS = 300
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Neededf for CorsHeader (accept connections from everywhere)
# CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'token',
    'x-device-id',
    'x-device-type',
    'x-push-id',
    'dataserviceversion',
    'maxdataserviceversion'
)
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

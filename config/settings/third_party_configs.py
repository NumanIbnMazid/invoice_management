import os
from pathlib import Path
from dotenv import load_dotenv

""" *** Project Directory Configurations *** """
BASE_DIR = Path(__file__).resolve().parent.parent.parent

""" # Project Third Party Configurations # """

""" *** Read Project Environment File *** """
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path)

"""
----------------------- * Django Allauth Configurations * -----------------------
"""
LOGIN_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'  # mandatory, optional, none
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_ADAPTER = 'config.adapter.CustomAccountAdapter'


"""
----------------------- * Django Memcache and Redis Cache Configurations * -----------------------
"""

REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

SESSIONS_ENGINE = 'django.contrib.sessions.backends.cache'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


"""
----------------------- * Django WhiteNoise Configurations * -----------------------
"""

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


"""
----------------------- * Django Debug Toolbar Configurations * -----------------------
"""

INTERNAL_IPS = [
    '127.0.0.1', '0.0.0.0', '167.172.87.22'
]

"""
----------------------- * Django Crispy Forms Configurations * -----------------------
"""

CRISPY_TEMPLATE_PACK = 'bootstrap4'
# CRISPY_CLASS_CONVERTERS = {'form-control': "form-control rounded-pill border-white input-box"}


"""
----------------------- * Django CK Editor Configuration * -----------------------
"""

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True

CKEDITOR_CONFIGS = {
    'default': {
        'uiColor': '#cdc9ff',
        'height': '100%',
        'width': '100%',
        # 'skin': 'moono',
        # 'skin': 'office2013',
        # 'toolbar_Basic': [
        #     ['Source', '-', 'Bold', 'Italic']
        # ],
        'toolbar_NMNckCustomToolbarConfig': [
            {'name': 'document', 'items': [
                'Print', '-', 'Templates', '-', 'Maximize', 'ShowBlocks', 'Preview']},
            {'name': 'clipboard', 'items': [
                'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo', 'Find', 'Replace', '-', 'SelectAll']},
            '/',
            {'name': 'basicstyles',
             'items': ['TextColor', 'BGColor', '-', 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       ]},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak']},
            '/',
            {'name': 'styles', 'items': [
                'Styles', 'Format', 'FontSize']},
        ],
        # 'toolbar': 'NMNckCustomToolbarConfig',  # put selected toolbar config here
        'toolbar': 'Basic',  # put selected toolbar config here
        'toolbar': 'full',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        'height': 500,
        'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
        "removePlugins": "exportpdf",
    }
}


"""
----------------------- * File Configuration * -----------------------
"""
ALLOWED_IMAGE_TYPES = ['.jpg', '.jpeg', '.png', '.svg']
MAX_UPLOAD_SIZE = 2621440

# File Validation Staffs
ALLOWED_JOB_APPLY_FILE_TYPES = ['.doc', '.docx', '.pdf']


"""
----------------------- * Select2 Configuration * -----------------------
"""

SELECT2_CACHE_BACKEND = "select2"

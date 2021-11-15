""" # Project Third Party Configurations # """


"""
----------------------- * Django Memcache Configurations * -----------------------
"""

SESSIONS_ENGINE = 'django.contrib.sessions.backends.cache'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
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
    '127.0.0.1', '0.0.0.0'
]

"""
----------------------- * Django Crispy Forms Configurations * -----------------------
"""

CRISPY_TEMPLATE_PACK = 'bootstrap4'
# CRISPY_CLASS_CONVERTERS = {'form-control': "form-control rounded-pill border-white input-box"}

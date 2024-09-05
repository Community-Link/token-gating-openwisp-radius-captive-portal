import os
import sys
from datetime import timedelta

from celery.schedules import crontab

TESTING = 'test' in sys.argv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'TzUQo/6sIHP#lZ=uB=Ox-aAxnB/1-Eof]g68VXao&dDMH4)Rff'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '127.0.0.1',
    '10.0.0.2',
    'openwisp2.openwisp.org',
]

CSRF_TRUSTED_ORIGINS = ['https://openwisp2.openwisp.org','https://*.127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.gis',
    # all-auth
    'django.contrib.sites',
    # overrides allauth templates
    # must precede allauth
    'openwisp_users.accounts',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_extensions',
    # openwisp2 modules
    'openwisp_users',
    'openwisp_controller.pki',
    'openwisp_controller.config',
    'openwisp_controller.geo',
    'openwisp_controller.connection',
    'openwisp_monitoring.monitoring',
    'openwisp_monitoring.device',
    'openwisp_monitoring.check',
    'nested_admin',
    'openwisp_notifications',
    'flat_json_widget',
    'openwisp_network_topology',
    'openwisp_firmware_upgrader',
    'openwisp_ipam',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'openwisp_radius',
    # openwisp2 admin theme
    # (must be loaded here)
    'openwisp_utils.admin_theme',
        'openwisp_utils.metric_collection',
        'admin_auto_filters',
    # admin
    'django.contrib.admin',
    'django.forms',
    # other dependencies
    'sortedm2m',
    'reversion',
    'leaflet',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework.authtoken',
    'django_filters',
    'private_storage',
    'drf_yasg',
    'channels',
    'pipeline',
    'import_export',
    'djcelery_email',
]

EXTENDED_APPS = [
    'django_x509',
    'django_loci',
]

PRIVATE_STORAGE_ROOT = os.path.join(BASE_DIR, 'private')

OPENWISP_FIRMWARE_UPGRADER_MAX_FILE_SIZE = 31457280

AUTH_USER_MODEL = 'openwisp_users.User'
SITE_ID = 1
LOGIN_REDIRECT_URL = 'admin:index'
ACCOUNT_LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'email_confirmation_success'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'email_confirmation_success'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'openwisp_utils.staticfiles.DependencyFinder',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
        'sesame.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'pipeline.middleware.MinifyHTMLMiddleware'
]

AUTHENTICATION_BACKENDS = [
    'openwisp_users.backends.UsersAuthenticationBackend',
]

OPENWISP_RADIUS_FREERADIUS_ALLOWED_HOSTS = ['127.0.0.1','10.0.0.1']
REST_AUTH = {
    'SESSION_LOGIN': False,
    'PASSWORD_RESET_SERIALIZER': 'openwisp_radius.api.serializers.PasswordResetSerializer',
    'REGISTER_SERIALIZER': 'openwisp_radius.api.serializers.RegisterSerializer',
}

# dj-rest-auth 3.0 changed the configuration settings.
# The below settings are kept for backward compatability with dj-rest-auth < 3.0
#
# Backward compatible settings begins
REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'openwisp_radius.api.serializers.PasswordResetSerializer',
}
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'openwisp_radius.api.serializers.RegisterSerializer',
}
# Backward compatible settings ends

# SMS settings
OPENWISP_RADIUS_SMS_TOKEN_MAX_IP_DAILY = 25
SENDSMS_BACKEND = 'sendsms.backends.console.SmsBackend'

OPENWISP_RADIUS_TRAFFIC_COUNTER_REPLY_NAME = 'pfSense-Max-Total-Octets'

# django-sesame configuration for magic sign-in links.
# Refer https://github.com/aaugustin/django-sesame#django-sesame.
AUTHENTICATION_BACKENDS += [
    'sesame.backends.ModelBackend',
]
SESAME_MAX_AGE = 1800

ROOT_URLCONF = 'openwisp2.urls'
OPENWISP_USERS_AUTH_API = True


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
            'group_expiry': 3600,
        },
    },
}
ASGI_APPLICATION = 'openwisp2.routing.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    'openwisp_utils.loaders.DependencyLoader'
                ]),
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'openwisp_utils.admin_theme.context_processor.menu_items',
                'openwisp_utils.admin_theme.context_processor.admin_theme_settings',
                'openwisp_notifications.context_processors.notification_api_settings',
            ],
        },
    },
]

# Run celery in eager mode using in-memory broker while running tests
if not TESTING:
    CELERY_TASK_ACKS_LATE = True
    CELERY_BROKER_URL = 'redis://localhost:6379/3'
else:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_BROKER_URL = 'memory://'

# Workaround for stalled migrate command
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'max_retries': 10,
}

CELERY_BEAT_SCHEDULE = {
    'delete_old_notifications': {
        'task': 'openwisp_notifications.tasks.delete_old_notifications',
        'schedule': crontab(**{ 'hour': 0, 'minute': 0 }),
        'args': (90,),
    },
    'run_checks': {
        'task': 'openwisp_monitoring.check.tasks.run_checks',
        'schedule': timedelta(minutes=5),
    },
    'deactivate_expired_users': {
        'task': 'openwisp_radius.tasks.deactivate_expired_users',
        'schedule': crontab(**{ 'hour': 0, 'minute': 5 }),
        'args': None,
        'relative': True,
    },
    'delete_old_radiusbatch_users': {
        'task': 'openwisp_radius.tasks.delete_old_radiusbatch_users',
        'schedule': crontab(**{ 'hour': 0, 'minute': 10 }),
        'args': [12],
        'relative': True,
    },
    'cleanup_stale_radacct': {
        'task': 'openwisp_radius.tasks.cleanup_stale_radacct',
        'schedule': crontab(**{ 'hour': 0, 'minute': 20 }),
        'args': [1],
        'relative': True,
    },
    'delete_old_postauth': {
        'task': 'openwisp_radius.tasks.delete_old_postauth',
        'schedule': crontab(**{ 'hour': 0, 'minute': 30 }),
        'args': [365],
        'relative': True,
    },
    'delete_old_radacct': {
        'task': 'openwisp_radius.tasks.delete_old_radacct',
        'schedule': crontab(**{ 'hour': 1, 'minute': 30 }),
            'args': [365],
            'relative': True,
        },
        'send_usage_metrics': {
        'task': 'openwisp_utils.metric_collection.tasks.send_usage_metrics',
        'schedule': timedelta(days=1),
    },
    'run_iperf3_checks': {
        'task': "openwisp_monitoring.check.tasks.run_checks",
        # https://docs.celeryq.dev/en/latest/userguide/periodic-tasks.html#crontab-schedules
        # Executes check every 5 mins from 00:00 AM to 6:00 AM (night)
        'schedule': crontab(minute="*/5", hour="*"),
        # Iperf3 check path
       'args': (["openwisp_monitoring.check.classes.Iperf3"],),
       'relative': True,
    },
}

CELERY_TASK_ROUTES = {
    # network operations, executed in the "network" queue
    'openwisp_controller.connection.tasks.*': {'queue': 'network'},
    # monitoring checks are executed in a dedicated "monitoring" queue
    'openwisp_monitoring.check.tasks.perform_check': {'queue': 'monitoring'},
    'openwisp_monitoring.monitoring.tasks.migrate_timeseries_database': {'queue': 'monitoring'},
    # firmware upgrade operations, executed in the "firmware_upgrader" queue
    'openwisp_firmware_upgrader.tasks.upgrade_firmware': {'queue': 'firmware_upgrader'},
    'openwisp_firmware_upgrader.tasks.batch_upgrade_operation': {'queue': 'firmware_upgrader'},
    # all other tasks are routed to the default queue (named "celery")
}

# FOR DJANGO REDIS

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'openwisp2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'openwisp_utils.db.backends.spatialite',
        'NAME': '/opt/openwisp2/db.sqlite3',
    }
}

SPATIALITE_LIBRARY_PATH = 'mod_spatialite.so'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {'NAME': 'openwisp_users.password_validation.PasswordReuseValidator'}
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_custom')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'


# django x509 settings
DJANGO_X509_DEFAULT_CERT_VALIDITY = 1825
DJANGO_X509_DEFAULT_CA_VALIDITY = 3650

LEAFLET_CONFIG = {}
# always disable RESET_VIEW button
LEAFLET_CONFIG['RESET_VIEW'] = False

# Set default email
DEFAULT_FROM_EMAIL = 'openwisp2@openwisp2.openwisp.org'
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
EMAIL_TIMEOUT = 10
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
        'verbose': {
            'format': '[%(levelname)s %(asctime)s] module: %(module)s, process: %(process)d, thread: %(thread)d\n%(message)s\n'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'main_log': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/openwisp2.log'),
            'maxBytes': 15728640,
            'backupCount': 3,
            'formatter': 'verbose'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': [
            'main_log',
            'console',
            'mail_admins',
        ]
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['main_log'],
            'propagate': False,
        }
    }
}

# HTML minification with django pipeline
PIPELINE = {'PIPELINE_ENABLED': True}
# static files minification and invalidation with django-compress-staticfiles
STATICFILES_STORAGE = 'openwisp_utils.storage.CompressStaticFilesStorage'
# GZIP compression is handled by nginx
BROTLI_STATIC_COMPRESSION = False
GZIP_STATIC_COMPRESSION = False


TIMESERIES_DATABASE = {
    'BACKEND': 'openwisp_monitoring.db.backends.influxdb',
    'USER': 'openwisp',
    'PASSWORD': 'openwisp',
    'NAME': 'openwisp2',
    'HOST': 'localhost',
    'PORT': '8086',
}
OPENWISP_MONITORING_DEFAULT_RETENTION_POLICY = '26280h0m0s'




TEST_RUNNER = 'openwisp_utils.metric_collection.tests.runner.MockRequestPostRunner'



OPENWISP_MONITORING_IPERF3_CHECK_CONFIG = {
    # 'org_pk' : {'host' : [], 'client_options' : {}}
    "b739471a-0f84-4fa3-9b27-546840136fa3":{
        # Some public iperf3 servers
        # https://iperf.fr/iperf-servers.php#public-servers
        "host": ["openwisp2.openwisp.org", "speedtest.mtl2.ca.leaseweb.net"],
        "client_options": {
            "port": 5201,
            "udp": {"bitrate": "30M"},
            "tcp": {"bitrate": "0"},
        },
    },
}


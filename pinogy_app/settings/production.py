from .base import *  # noqa
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

IS_LOCAL = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": "INFO",
        "handlers": ["default", "db_log"]
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler"
        },
        'db_log': {
            'level': 'ERROR',
            'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
        },
        "info_db_log": {
            "level": "INFO",
            "class": "django_db_logger.db_log_handler.DatabaseLogHandler",
        },
    },
    "loggers": {
        "django": {
            "level": "INFO",
            "propagate": True
        },
        "shop": {
            "handlers": ["db_log"],
            "level": "INFO",
            "propagate": False,
        },
        'django.request': { # logging 500 errors to database
            'handlers': ['db_log'],
            'level': 'ERROR',
            'propagate': False,
        },
        "debug_logger": {
            "handlers": ["info_db_log"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

DEPLOYED_VERSION = "pgy-websites@IMAGE_TAG"
HOST_NAME = os.environ.get('HOSTNAME')
API_LAYWAY = os.environ.get('API_LAYWAY')

if not DEBUG:
    sentry_sdk.init(
        dsn="https://4a68cef572fe44c49e0e261bec52817e@o60910.ingest.sentry.io/1215852",
        integrations=[DjangoIntegration()],
        release=DEPLOYED_VERSION,
        environment=REDIS_PREFIX,
        traces_sample_rate=0.01,
        send_default_pii=True
    )

PINOGY_API_HOST = os.environ.get("PINOGY_API_HOST")
PINOGY_ACCESS_KEY = os.environ.get("PINOGY_ACCESS_KEY")
PINOGY_SECRET_KEY = os.environ.get("PINOGY_SECRET_KEY")
PINOGY_API_PASS = os.environ.get("PINOGY_API_PASS")

# Production card connect URL
CARDCONNECT_SERVER_URL = "https://boltgw.cardconnect.com:8443"

# Google reviews key
GOOGLE_REVIEWS_KEY = "AIzaSyCQLZfRcIKmCo6--y2pED4YkWUx5oeT-8g"
from .base import *  # noqa
from .base import env  # noqa

IS_LOCAL = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "==== %(levelname)s %(asctime)s %(module)s %(message)s ===="
        },
        "simple": {
            "format": "==== %(levelname)s %(asctime)s %(module)s %(message)s ===="
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "db_log": {
            "level": "INFO",
            "class": "django_db_logger.db_log_handler.DatabaseLogHandler",
        },
        "info_db_log": {
            "level": "INFO",
            "class": "django_db_logger.db_log_handler.DatabaseLogHandler",
        },
    },
    "root": {"level": "INFO", "handlers": ["default"]},
    "loggers": {
        "django": {"level": "INFO", "propagate": True},
        "debug_logger": {
            "handlers": ["info_db_log"],
            "level": "INFO",
            "propagate": False,
        },
        "shop": {
            "handlers": ["db_log"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {  # logging 500 errors to database
            "handlers": ["db_log", "default"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

THUMBNAIL_DEBUG = True

DEPLOYED_VERSION = "pgy-websites@22.12.01"
HOST_NAME = os.environ.get("HOSTNAME", "Local Host")

if os.environ.get("DATABASE_PATH"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "DISABLE_SERVER_SIDE_CURSORS": True,
            "OPTIONS": {"options": f"-c search_path={os.environ.get('DATABASE_PATH')}"},
            "NAME": os.environ.get("POSTGRES_DB") or os.environ.get("DATABASE_NAME"),
            "USER": os.environ.get("POSTGRES_USER") or os.environ.get("DATABASE_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD")
            or os.environ.get("DATABASE_PASSWORD"),
            "HOST": os.environ.get("POSTGRES_HOST") or os.environ.get("DATABASE_HOST"),
            "PORT": os.environ.get("POSTGRES_PORT") or os.environ.get("DATABASE_PORT"),
        },
    }

# Shop
CARDCONNECT_SERVER_URL = "https://boltgw.cardconnect.com:6443"

# Google reviews key
GOOGLE_REVIEWS_KEY = "" # Do not keep key here

# ==============================================
#   Pinogy API access key and other credentials
# ==============================================

# 0002 thefamilypuppy.com
# PINOGY_API_HOST = "https://api-corepos-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "xNLV8sfmN98K7sShRK32"
# PINOGY_SECRET_KEY = "k8gcjb2jGfzJQbGL3fSF"
# PINOGY_API_PASS = "ka83jf43865"
# API_LAYWAY = "https://api-corepos-v1.pinogy.com"

# 0005 puppylandsanantonio.com/puppylandtexas
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "xWZkhF7QLsrqWRxmDzvb"
# PINOGY_SECRET_KEY = "5PqKwMm5M6NHSBQst9s6"
# PINOGY_API_PASS = "2023-10-2516:36:215"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 0032 myhealthypetstores.com
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "5k8jWQmntLjDRStCLSKj"
# PINOGY_SECRET_KEY = "WnQz48jXSfzCWGWqXKxD"
# PINOGY_API_PASS = "ka83jf151601006"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 0036 - CB Pet Market
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "gsVF3dGv6zVMzZGdjrD6"
# PINOGY_SECRET_KEY = "XL3LR8zsKNgBdZXRZKsG"
# PINOGY_API_PASS = "2021-07-2313:51:365"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 0042 theperfactpupstore
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "TwjfT6wMBHM2L2wqN8NR"
# PINOGY_SECRET_KEY = "VPDf8XQG4D8sRD3gJSMb"
# PINOGY_API_PASS = "2021-10-1916:54:395"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 055 - Staright Line
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "GtM8VzBLvThrr4NzxxBn"
# PINOGY_SECRET_KEY = "CvCpwxv9GVThzXRt59VK"
# PINOGY_API_PASS = "2021-12-1710:39:515"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 0056 Demo Shop
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "bPKkKkmf8NQSG8B7vDKg"
# PINOGY_SECRET_KEY = "svm6xGZCrtfHZsMt7ZKC"
# PINOGY_API_PASS = "2021-12-2410:44:38179"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 0077 - Wag heaven
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "q54SpsGnxSVc6ZJ5WLzK"
# PINOGY_SECRET_KEY = "2xH76nS6hz28LfjR7Gj6"
# PINOGY_API_PASS = "2022-02-2816:32:475"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 105 - Hooves & Paws
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "v2nQ48D6gVf358gZRQjq"
# PINOGY_SECRET_KEY = "SKfStq3mQGX5DHdHcJRC"
# PINOGY_API_PASS = "2022-11-1409:18:475"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 115 - Little Puppies Online
# PINOGY_API_HOST = "https://us00mt15.pinogy.net"
# PINOGY_ACCESS_KEY = "3nfJSF2zxZMJLhW9WHZN"
# PINOGY_SECRET_KEY = "kNKCKvVpGQD3Tm9Jdz2S"
# PINOGY_API_PASS = "2023-02-2417:27:005"
# API_LAYWAY = "https://us00mt15.pinogy.net"

# 120 Julz Animal Houz
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "2nv3dHLD72Sj4SNGkkch"
# PINOGY_SECRET_KEY = "8x3dbr4QxjhvPvvt8Xwg"
# PINOGY_API_PASS = "2023-01-0315:20:277"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 121 - Summit Zoo
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "fQWwZLjSSVTXFNXvLFzF"
# PINOGY_SECRET_KEY = "dR42ZVXBNbgvZrrXqTzR"
# PINOGY_API_PASS = "2023-01-2416:19:475"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 122 - A Dog's Dream
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "nzqCPTX8XfKJBtps5TRG"
# PINOGY_SECRET_KEY = "hPBGF2Hm3RmRfrFPK6b5"
# PINOGY_API_PASS = "2023-06-2811:17:095"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 124 - Shake-A-Paw
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "DR3nJxk5XNVFDWJpZMFb"
# PINOGY_SECRET_KEY = "tRmCfpQmQckN5dFjMp5r"
# PINOGY_API_PASS = "2023-02-0315:46:545"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 126 - WoofMeow
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "Q2j2P4WLCQmVg2VHZ5jD"
# PINOGY_SECRET_KEY = "zP865wfKTSFckP4ZHgqF"
# PINOGY_API_PASS = "2023-04-1809:31:595"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 127 - Pet City
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "tNcGcfQnXL9Fbx2Q5QLf"
# PINOGY_SECRET_KEY = "w8Bv4Vwjjntxdj9BpL8W"
# PINOGY_API_PASS = "2021-12-0313:34:316"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 128 - Waggles Pet
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "5cSBPF3nXp8zZMdTHBtt"
# PINOGY_SECRET_KEY = "4bjz4NmxjkpjHTgxjBDw"
# PINOGY_API_PASS = "2022-02-0112:08:015"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 129 - Waggles Puppies Franchise
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "wXF4BXxNQbqT2HwhGNbF"
# PINOGY_SECRET_KEY = "HDNdq2DpJDJST4rrg5Wz"
# PINOGY_API_PASS = "2023-05-1717:46:305"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 130 - Corporate Lawyer/Jay Site
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "VGF2J2mJBr29vHvCvvX7"
# PINOGY_SECRET_KEY = "sFHszgH4v8nBz2rLBxQQ"
# PINOGY_API_PASS = "2023-05-3009:20:345"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 133 - Purely Puppies
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "WBLcZZKwDKJCMB5pN45z"
# PINOGY_SECRET_KEY = "6fcgWh98qDX2WFh5KvNj"
# PINOGY_API_PASS = "2023-07-0319:38:255"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 138 - Straightline Kennels
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "GtM8VzBLvThrr4NzxxBn"
# PINOGY_SECRET_KEY = "CvCpwxv9GVThzXRt59VK"
# PINOGY_API_PASS = "2021-12-1710:39:515"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 139
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "qsXqT6sGkpZ7tDwtQ2s2"
# PINOGY_SECRET_KEY = "SHbwSqsJhdVZhptmB557"
# PINOGY_API_PASS = "2023-08-0815:26:125"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 142 Pet express
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "WvFpw2n8fDbvCgXrBR5z"
# PINOGY_SECRET_KEY = "Sd2TTCCj67WVdtHpM3g2"
# PINOGY_API_PASS = "2021-12-0313:46:336"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 147
PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
PINOGY_ACCESS_KEY = "W43C4FjTpbCv9Npx8NJT"
PINOGY_SECRET_KEY = "shzZ7NT3GJ8S4K38SmsX"
PINOGY_API_PASS = "2023-11-0910:02:35179"
API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 0149
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "NXnvJKHS9Q8sND5vqRWM"
# PINOGY_SECRET_KEY = "6K3hG7mjjpzv8K3zdzPb"
# PINOGY_API_PASS = "2023-10-2614:04:106"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 0152, 0037 PuppyDreams
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "Q49PtcHw8Tz3sBSgQt7g"
# PINOGY_SECRET_KEY = "p78vKGDzrvLb85hhXhd2"
# PINOGY_API_PASS = "2021-07-2611:17:165"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 153
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "PbMjBSKGLd9cgRcNsX4x"
# PINOGY_SECRET_KEY = "XXk6MqmXDZcsTNKc3QMQ"
# PINOGY_API_PASS = "2023-12-1909:28:535"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 166 adventurepets
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "ptGDc8CX2vMG8dMKDNtM"
# PINOGY_SECRET_KEY = "WhxKkbHkS4v2GVFtJrSG"
# PINOGY_API_PASS = "2024-02-1211:42:479"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 169
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "qCQVh4c3hvNDCMmHXqGH"
# PINOGY_SECRET_KEY = "jgWhbbq7xgPdFjBmKBpP"
# PINOGY_API_PASS = "2022-08-2913:11:555"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 170
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "djbvKs9NmTmNfgkqQDkP"
# PINOGY_SECRET_KEY = "VJNsrcNh5w7mdmMWfj4L"
# PINOGY_API_PASS = "ka83jf41569"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 171
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "fRggnBpmJ2xxQTFKrH3G"
# PINOGY_SECRET_KEY = "QWr2jR6GH6VZ8zCPxkVd"
# PINOGY_API_PASS = "2024-03-1317:34:496"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 172
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "pC6VZhpGvN4dgCvb4fkL"
# PINOGY_SECRET_KEY = "N6fVNrJbtmX3SNR6Vbcv"
# PINOGY_API_PASS = "2024-03-0713:06:545"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 187
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "w7CmJLtQMNTc2g5293hP"
# PINOGY_SECRET_KEY = "jXwm8Cnh2pMxPcgCHq8d"
# PINOGY_API_PASS = "2024-05-1309:03:376"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 188 wagglescharlotte
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "9jjb4gZ4RWjnKcPKrjvV"
# PINOGY_SECRET_KEY = "PR24vQdgv6JqpGBpJ2F9"
# PINOGY_API_PASS = "2024-05-2417:20:445"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 191 petlandwichitawest
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "fpm5z2LSNXztj34PqPqn"
# PINOGY_SECRET_KEY = "bzccxGb8xZFQMFwwjJg4"
# PINOGY_API_PASS = "2024-06-1417:27:126"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 199 petlandwichitawest
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "fpm5z2LSNXztj34PqPqn"
# PINOGY_SECRET_KEY = "bzccxGb8xZFQMFwwjJg4"
# PINOGY_API_PASS = "2024-06-1417:27:126"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 200
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "jW9RMZ7N5JdjnRDbrJVv"
# PINOGY_SECRET_KEY = "tJQMXvMGK3MbZtcNrts4"
# PINOGY_API_PASS = "2024-08-2614:50:495"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com"

# 201
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "scJtZs8bLzTpghVkJXNG"
# PINOGY_SECRET_KEY = "LCtRRXDzVtm2wHbV88w8"
# PINOGY_API_PASS = "2024-09-1211:26:265"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com" 

# 204
# PINOGY_API_HOST = "https://api-coreposweb-v1.pinogy.com"
# PINOGY_ACCESS_KEY = "HbRBj2HDsmSWLb2DMpqt"
# PINOGY_SECRET_KEY = "3QJ284b99R5RL25cQsDs"
# PINOGY_API_PASS = "2024-09-0511:28:277"
# API_LAYWAY = "https://api-coreposweb-v1.pinogy.com" 


#0995
# # Development env #
# PINOGY_API_HOST = "https://api-corepos-v1-dev.pinogy.net"
# PINOGY_ACCESS_KEY = "sbrdD5BttKqF89FhHmGw"
# PINOGY_SECRET_KEY = "8M35PRjH96f5bWzfDKnV"
# PINOGY_API_PASS = "ka83jf733028263"
# API_LAYWAY = "https://api-corepos-v1-dev.pinogy.net"

# Deploying shop changes
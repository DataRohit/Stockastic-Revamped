# Imports
from pathlib import Path

import environ

# Base directory of the Django project
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# App directory of the Django project
APPS_DIR = BASE_DIR / "apps"

# Initialize environment variables
env = environ.Env()

# Read the environment variables from the .env file
READ_DOT_ENV_FILE = env.bool(var="DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    env.read_env(str(BASE_DIR / ".env"))

# Set auth user model
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = "account.User"

# General
# ------------------------------------------------------------------------------
DEBUG = env.bool(var="DJANGO_DEBUG", default=False)
SECRET_KEY = env.str(
    var="DJANGO_SECRET_KEY",
    default="&j5+b5hje=q_k*=(_1q+yg))f2q4=e=12b@#-0hz2nipu%zv%y74!vws_$-ohn-oga10pq)15=l!8ef9b7m3x#0mw0fq28-$-m95",
)
ALLOWED_HOSTS = env.list(var="DJANGO_ALLOWED_HOSTS", default=["127.0.0.1"])
CSRF_TRUSTED_ORIGINS = env.list(
    var="DJANGO_CSRF_TRUSTED_ORIGINS",
    default=[
        "http://127.0.0.1:8000",
    ],
)
CORS_ALLOWED_ORIGINS = env.list(
    var="DJANGO_CORS_ALLOWED_ORIGINS",
    default=[
        "http://127.0.0.1:8000",
    ],
)

# Site settings
# ------------------------------------------------------------------------------
SITE_ID = 1
SITE_NAME = env.str(var="SITE_NAME", default="Stockastic")

# Internationalization
# ------------------------------------------------------------------------------
TIME_ZONE = "Asia/Kolkata"
LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_TZ = True

# Databases
# ------------------------------------------------------------------------------
DATABASES = {"default": env.db(var="DATABASE_URL", default="sqlite:///db.sqlite3")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Urls
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
ASGI_APPLICATION = "config.asgi.application"

# Apps
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django_admin_dracula",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "corsheaders",
    "storages",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "health_check.contrib.s3boto3_storage",
    "health_check.contrib.redis",
    "silk",
    "widget_tweaks",
    "django_extensions",
    "django_filters",
    "channels",
    "django_celery_beat",
]
LOCAL_APPS = [
    "apps.account",
    "apps.core",
    "apps.socket",
    "apps.stock",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Authentication
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Set authentication urls
# ------------------------------------------------------------------------------
LOGIN_URL = "account:login"
LOGIN_REDIRECT_URL = "core:dashboard"
LOGOUT_REDIRECT_URL = "core:home"

# Passwords
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Middleware
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silk.middleware.SilkyMiddleware",
]

# Templates
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Security
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

# Admin
# ------------------------------------------------------------------------------
ADMIN_URL = "admin/"

# Logging
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Redis settings
# ------------------------------------------------------------------------------
REDIS_URL = env.str("REDIS_URL", default="redis://localhost:6379/0")

# Cache settings
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "KEY_PREFIX": "stockastic",
        },
        "TIMEOUT": 60 * 15,
    },
}


# Channel layers (e.g., using Redis for real-time communication)
# ------------------------------------------------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (
                    env.str("REDIS_HOST", default="127.0.0.1"),
                    env.int("REDIS_PORT", default=6379),
                )
            ],
        },
    },
}


# MinIO settings
# ------------------------------------------------------------------------------
MINIO_STORAGE_ENDPOINT = env.str("MINIO_STORAGE_ENDPOINT", "localhost:9000")
MINIO_STORAGE_DOMAIN = env.str("MINIO_STORAGE_DOMAIN", "localhost:8080")
MINIO_STORAGE_ACCESS_KEY = env.str("MINIO_STORAGE_ACCESS_KEY")
MINIO_STORAGE_SECRET_KEY = env.str("MINIO_STORAGE_SECRET_KEY")
MINIO_STORAGE_USE_HTTPS = False

# AWS S3 settings (assuming MinIO setup)
# ------------------------------------------------------------------------------
# MinIO Endpoint Configuration
AWS_S3_ENDPOINT_URL = f"http://{MINIO_STORAGE_ENDPOINT}"

# Access Credentials
AWS_ACCESS_KEY_ID = MINIO_STORAGE_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = MINIO_STORAGE_SECRET_KEY

# Bucket Configuration
AWS_STORAGE_BUCKET_NAME = "stockastic"
AWS_S3_REGION_NAME = "us-east-1"

# Signature and ACL Settings
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = "private"

# File Overwrite and Query String Settings
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = True

# Custom Domain Configuration
AWS_S3_CUSTOM_DOMAIN = f"{MINIO_STORAGE_DOMAIN}/minio/storage/{AWS_STORAGE_BUCKET_NAME}"


# Static files settings
# ------------------------------------------------------------------------------
STATIC_URL = f"http://{MINIO_STORAGE_DOMAIN}/{AWS_STORAGE_BUCKET_NAME}/static/"
STATICFILES_STORAGE = "config.storage.StaticStorage"

# Media files settings
# ------------------------------------------------------------------------------
MEDIA_URL = f"http://{MINIO_STORAGE_DOMAIN}/{AWS_STORAGE_BUCKET_NAME}/media/"
DEFAULT_FILE_STORAGE = "config.storage.MediaStorage"

# Static files finders and directories
# ------------------------------------------------------------------------------
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# Celery
# ------------------------------------------------------------------------------
# Timezone Settings
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

# Broker and Backend Configuration
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# Result Backend Settings
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
CELERY_RESULT_BACKEND_MAX_RETRIES = 10

# Serialization Settings
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# Task Time Limits
CELERY_TASK_TIME_LIMIT = 5 * 60  # 5 minutes
CELERY_TASK_SOFT_TIME_LIMIT = 60  # 1 minute

# Scheduler Settings
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Task Event Settings
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True

# Beat Schedule Configuration
CELERY_BEAT_SCHEDULE = {}

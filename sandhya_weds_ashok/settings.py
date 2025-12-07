"""
Django settings for sandhya_weds_ashok project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# Security / Env
# -------------------------------------------------------------------

# For local dev, this default is fine; for prod we'll override via env
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY",)

# DJANGO_DEBUG = "True" / "False"
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# Comma-separated list in env; "*" for dev is okay
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

# -------------------------------------------------------------------
# Application definition
# -------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "weddingpage",
    "webpack_loader",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "sandhya_weds_ashok.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sandhya_weds_ashok.wsgi.application"

# -------------------------------------------------------------------
# Database
# -------------------------------------------------------------------
# Local default = your Postgres weddingdb
# On Render, we'll override via env if needed

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),  # set for prod
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
    }
}

# -------------------------------------------------------------------
# Password validation
# -------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# -------------------------------------------------------------------
# Internationalization
# -------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# Webpack loader
# -------------------------------------------------------------------

WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "bundles/",
        "STATS_FILE": BASE_DIR / "webpack-stats.json",
    }
}

# -------------------------------------------------------------------
# Static files
# -------------------------------------------------------------------
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# Corrected Region Name format: use the code, not the descriptive name
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME') 

# Configure the S3 domain URL structure
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_SECURE_URLS = True # Use HTTPS

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# 2. Static Files Storage (CSS/JS/Bundles)
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"


# Point STATIC_URL to the S3 bucket URL
STATIC_URL = '/static/'

# Where collectstatic puts all static files in prod
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "frontend/static",
    BASE_DIR / "static",
]

 # e.g., 'us-west-2'
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

import dj_database_url
import os
from pathlib import Path
from decouple import config

# ------------------------------
# Paths
# ------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------
# Security
# ------------------------------
SECRET_KEY = config("SECRET_KEY", default="your-secret-key")  # change in production
DEBUG = config("DEBUG", default=True, cast=bool)  # True for local dev, False for prod
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "pharmacies-saas2-1.onrender.com"]

# ------------------------------
# Installed apps
# ------------------------------
INSTALLED_APPS = [
    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "django_extensions",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "whitenoise.runserver_nostatic",

    # Project apps
    "apps.users.apps.UsersConfig",
    "apps.deliveries.apps.DeliveriesConfig",
    "apps.pharmacies",
    "platform_config_app",
    "apps.api",
    "apps.orders",
    "apps.products",
    "apps.payments",
    "apps.symptoms",
    "apps.consumers",
    "apps.riders",
    "apps.tracking",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------
# Middleware
# ------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be at top
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # for static files in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ------------------------------
# URLs & WSGI
# ------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ------------------------------
# Templates
# ------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ------------------------------
# Database (PostgreSQL)
# ------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "pharmacies_db",
        "USER": "ihabib_4",
        "PASSWORD": "<password>",
        "HOST": "localhost",
        "PORT": "5432",
        "OPTIONS": {
            "options": "-c search_path=public"
        },
    }
}

# ------------------------------
# Authentication
# ------------------------------
AUTH_USER_MODEL = "users.CustomUser"

# ------------------------------
# Static files
# ------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ------------------------------
# Django REST Framework
# ------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

# ------------------------------
# CORS
# ------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# ------------------------------
# Payment (Tigo Pesa sandbox)
# ------------------------------
TIGO_API_URL = "https://sandbox.tigoapi.com/v1/payment"
TIGO_API_KEY = config("TIGO_API_KEY", default="your_sandbox_api_key_here")
TIGO_SHORTCODE = config("TIGO_SHORTCODE", default="123456")
TIGO_CALLBACK_URL = config(
    "TIGO_CALLBACK_URL", default="http://127.0.0.1:8000/api/payments/callback/"
)

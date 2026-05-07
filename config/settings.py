import os
from pathlib import Path
from datetime import timedelta
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


# ------------------------------
# SECURITY
# ------------------------------
SECRET_KEY = config("SECRET_KEY", default="your-secret-key")
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "192.168.0.177",
    "192.168.1.10",
    "0.0.0.0",
    "pharmacies-saas2-1.onrender.com",
]


# ------------------------------
# APPS
# ------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # THIRD PARTY
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "django_extensions",
    "whitenoise.runserver_nostatic",

    # LOCAL APPS
    "platform_config_app.apps.PlatformConfigAppConfig",
    "platform_settings.apps.PlatformSettingsConfig",

    "apps.users.apps.UsersConfig",
    "apps.deliveries.apps.DeliveriesConfig",
    "apps.pharmacies.apps.PharmaciesConfig",
    "apps.products.apps.ProductsConfig",
    "apps.orders.apps.OrdersConfig",
    "apps.payments.apps.PaymentsConfig",
    "apps.symptoms.apps.SymptomsConfig",
    "apps.consumers.apps.ConsumersConfig",
    "apps.riders.apps.RidersConfig",
    "apps.tracking.apps.TrackingConfig",
    "apps.api.apps.ApiConfig",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ------------------------------
# MIDDLEWARE
# ------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    # Keep CSRF enabled for admin safety
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # ⚠️ CUSTOM MIDDLEWARE (potential risk point)
    "apps.tracking.middleware.AuditMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"


# ------------------------------
# TEMPLATES
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
# DATABASE
# ------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}


# ------------------------------
# AUTH
# ------------------------------
AUTH_USER_MODEL = "users.CustomUser"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]


# ------------------------------
# REST FRAMEWORK
# ------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
}


# ------------------------------
# JWT
# ------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# ------------------------------
# STATIC FILES
# ------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ------------------------------
# CORS
# ------------------------------
CORS_ALLOW_ALL_ORIGINS = True


# ------------------------------
# SECURITY (PRODUCTION)
# ------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# ------------------------------
# PAYMENT (Tigo Pesa)
# ------------------------------
TIGO_API_URL = config("TIGO_API_URL", default="https://sandbox.tigoapi.com")
TIGO_API_KEY = config("TIGO_API_KEY", default="")
TIGO_MERCHANT_ID = config("TIGO_MERCHANT_ID", default="")

TIGO_CALLBACK_URL = config(
    "TIGO_CALLBACK_URL",
    default="http://127.0.0.1:8000/api/payments/tigo/callback/",
)

"""
Django settings for VVswinss.

Configuración base para desarrollo y producción.
Django 5.2 LTS.
"""

from pathlib import Path
import environ

# ============================================================
# BASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

env = environ.Env(
    DEBUG=(bool, False),
    EMAIL_USE_TLS=(bool, True),
    SECURE_SSL_REDIRECT=(bool, False),
    SESSION_COOKIE_SECURE=(bool, False),
    CSRF_COOKIE_SECURE=(bool, False),
)

environ.Env.read_env(BASE_DIR / ".env")

# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG", default=False)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["127.0.0.1", "localhost"],
)

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[],
)

SECURE_SSL_REDIRECT = env.bool(
    "SECURE_SSL_REDIRECT",
    default=False,
)

SESSION_COOKIE_SECURE = env.bool(
    "SESSION_COOKIE_SECURE",
    default=False,
)

CSRF_COOKIE_SECURE = env.bool(
    "CSRF_COOKIE_SECURE",
    default=False,
)

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

# Permite que servicios externos como YouTube reciban
# el origen del sitio al cargar contenido embebido.
# Evita el Error 153 del reproductor de YouTube.
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # VVswiss
    "core",
    "services",
    "projects",
    "blog",
    "contact",
]

# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ============================================================
# URLS / WSGI
# ============================================================

ROOT_URLCONF = "vvswinss.urls"
WSGI_APPLICATION = "vvswinss.wsgi.application"

# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "services.context_processors.services_menu",
                "core.context_processors.global_site",
            ],
        },
    },
]

# ============================================================
# DATABASE
# ============================================================

DATABASES = {
    "default": {
        "ENGINE": env(
            "DB_ENGINE",
            default="django.db.backends.postgresql",
        ),
        "NAME": env("DB_NAME", default="vvswinss"),
        "USER": env("DB_USER", default="vvswinss_user"),
        "PASSWORD": env("DB_PASSWORD", default=""),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
    }
}

# ============================================================
# EMAIL
# ============================================================

EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)

EMAIL_HOST = env(
    "EMAIL_HOST",
    default="",
)

EMAIL_PORT = env.int(
    "EMAIL_PORT",
    default=2525,
)

EMAIL_USE_TLS = env.bool(
    "EMAIL_USE_TLS",
    default=True,
)

EMAIL_HOST_USER = env(
    "EMAIL_HOST_USER",
    default="",
)

EMAIL_HOST_PASSWORD = env(
    "EMAIL_HOST_PASSWORD",
    default="",
)

DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL",
    default="V&V Swiss Services <contact@tudominio.ch>",
)

EMAIL_TIMEOUT = env.int(
    "EMAIL_TIMEOUT",
    default=10,
)

# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

# ============================================================
# INTERNATIONALIZATION
# ============================================================

DEFAULT_LANGUAGE = env(
    "DEFAULT_LANGUAGE",
    default="fr",
)

LANGUAGE_CODE = DEFAULT_LANGUAGE

LANGUAGES = [
    ("fr", "Français"),
    ("de", "Deutsch"),
    ("it", "Italiano"),
    ("en", "English"),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

TIME_ZONE = "Europe/Zurich"

USE_I18N = True
USE_TZ = True

# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ============================================================
# WEBSITE
# ============================================================

SITE_URL = env(
    "SITE_URL",
    default="http://127.0.0.1:8000",
)

# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
X_FRAME_OPTIONS = "SAMEORIGIN"

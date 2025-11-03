import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-^^^v)rv3al^5jb@$@ff-_x7wk9uwj-+f*^2n7an*kb0lv1u(a1"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all hosts during development. For production, specify allowed hosts.
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "courses",
    "notes",
    "routine",
    "users",
    # Add your 'courses' app here
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "MyProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates")
        ],  # Look for templates in the 'templates' folder
        "APP_DIRS": True,  # Enable Django to look for templates in app-specific 'templates' folders
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",  # Add this for static files
            ],
        },
    },
]

WSGI_APPLICATION = "MyProject.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # SQLite database engine
        "NAME": BASE_DIR / "db.sqlite3",  # Path to the SQLite database file
    }
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = "en-us"  # Default language
TIME_ZONE = "UTC"  # Default time zone
USE_I18N = True  # Enable internationalization
USE_TZ = True  # Enable time zone support
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]  # Look for static files in the 'static' folder

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
#####################################################################################settings.py
AUTH_USER_MODEL = "users.CustomUser"
LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "users:profile"

import os

# SSLCommerz payment gateway settings (prefer environment variables in prod)
SSLCOMMERZ = {
    # prefer environment variables in production; fallback to sandbox test creds
    "STORE_ID": os.getenv("SSLCOMMERZ_STORE_ID", "letsl68f3ded56916e"),
    "STORE_PASS": os.getenv("SSLCOMMERZ_STORE_PASS", "letsl68f3ded56916e@ssl"),
    # set to 'False' in production environment variables when going live
    "IS_SANDBOX": os.getenv("SSLCOMMERZ_IS_SANDBOX", "True").lower() in ("1", "true", "yes"),
}

# Derive API endpoints for convenience
if SSLCOMMERZ.get("IS_SANDBOX"):
    SSLCOMMERZ["SESSION_API"] = "https://sandbox.sslcommerz.com/gwprocess/v3/api.php"
    SSLCOMMERZ["VALIDATION_API"] = (
        "https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php"
    )
    # test phone to use when sandboxing (fallback when user has no phone)
    SSLCOMMERZ["TEST_CUSTOMER_PHONE"] = os.getenv("SSLCOMMERZ_TEST_CUSTOMER_PHONE", "01700000000")
else:
    SSLCOMMERZ["SESSION_API"] = "https://securepay.sslcommerz.com/gwprocess/v3/api.php"
    SSLCOMMERZ["VALIDATION_API"] = (
        "https://securepay.sslcommerz.com/validator/api/validationserverAPI.php"
    )
    SSLCOMMERZ["TEST_CUSTOMER_PHONE"] = os.getenv("SSLCOMMERZ_TEST_CUSTOMER_PHONE", "")

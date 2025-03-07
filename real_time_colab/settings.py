# settings.py
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p4w6*dh_7g#*e%xov-^^9bpbkwsnb#)xto3n-w^^_*ru16ur1s'  # Replace with a secure key in production

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # Set to False in production

ALLOWED_HOSTS = ['*', 'geinotech-colab.onrender.com', "lucky-worlds-crash.loca.lt"]  # Update with your domain in production
CSRF_TRUSTED_ORIGINS = [
    "https://lucky-worlds-crash.loca.lt"
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',  # Ensure this is included
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',  # Add Django Channels
    'real_real_time_app',  # Your app
]

# settings.py
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis://localhost:6379/0")],  # Replace with your Redis server URL
        },
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Ensure this is included
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'real_time_colab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'real_time_colab.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django Channels Configuration
ASGI_APPLICATION = 'real_time_colab.asgi.application'

# Session Configuration (Required for WebSocket authentication)
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"  # Use signed cookies for sessions
SESSION_COOKIE_NAME = "real_time_colab_session"  # Custom session cookie name
SESSION_COOKIE_AGE = 1209600  

# Static and Media Files (Optional)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # For production
MEDIA_URL = '/media/'  # For file uploads
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # For file uploads

# Logging Configuration (Optional)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
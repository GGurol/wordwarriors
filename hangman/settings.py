"""
Django settings for hangman project.
Updated for Django 5.2 and modern best practices.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Core Security Settings ---

# SECURITY WARNING: It's a best practice to load the secret key from an environment variable.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-=%*dlm9+3_rhf#l3r0th@lk&s)-w+mvi94@vee(snp$rk1ey^h')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# For development, '*' is fine. For production, be specific.
ALLOWED_HOSTS = ["*"]

# --- Application Definition ---

INSTALLED_APPS = [
    'game',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hangman.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # It's a good practice to have a project-level 'templates' directory
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'hangman.wsgi.application'


# --- Database Configuration ---

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Custom User Model ---
# This line is critical and has been preserved.
AUTH_USER_MODEL = "game.User"

# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static & Media Files ---
STATIC_URL = '/static/'
# Directory where 'collectstatic' will place all files for production.
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Additional locations the staticfiles app will traverse for development.
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# For user-uploaded files (e.g., profile pictures).
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- Default Primary Key Field Type ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
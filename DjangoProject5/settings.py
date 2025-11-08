from pathlib import Path
from decouple import config  # 👈 importa decouple
import os
from dotenv import load_dotenv  # 👈 importa dotenv
import dj_database_url

# Load .env used for local/dev secrets (openai.env is gitignored)
load_dotenv(os.path.join(Path(__file__).resolve().parent.parent, 'openai.env'))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="changeme")  # puedes mover también tu secret aquí
# By default in production DEBUG should be False
DEBUG = config("DEBUG", default=False, cast=bool)

# Read ALLOWED_HOSTS from env to make deployments (Render/Heroku) configurable
raw_allowed = config('ALLOWED_HOSTS', default='54.160.195.196,localhost,127.0.0.1,https://proyecto-e-1.onrender.com,.onrender.com')
ALLOWED_HOSTS = [h.strip() for h in raw_allowed.split(',') if h.strip()]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
    'ia',
    "crispy_forms",
    "crispy_bootstrap5",
    "productos",
    'widget_tweaks'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DjangoProject5.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoProject5.wsgi.application'

# Database configuration
# Default to local SQLite but allow DATABASE_URL override (Postgres on Render)
default_sqlite = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
DATABASES = {
    'default': dj_database_url.parse(config('DATABASE_URL', default=default_sqlite), conn_max_age=600)
}

LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# Directorio para los archivos estáticos recolectados por collectstatic (producción/Docker)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise configuration: allow Gunicorn to serve static files directly from STATIC_ROOT
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
# Archivos multimedia (imágenes de productos, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

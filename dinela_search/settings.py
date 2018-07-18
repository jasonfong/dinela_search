import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'REPLACE_ON_DEPLOYMENT-ea697ec7-9504-4aeb-a987-4443dfc983ff'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dinela_search',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'dinela_search.urls'

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

WSGI_APPLICATION = 'dinela_search.wsgi.application'

DATABASES = {
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DINELA_BASEURL = "https://www.discoverlosangeles.com/dinela-los-angeles-restaurant-week"
DINELA_INDEX_FILE_PATH = "data/index.html"
GCS_BUCKET = "YOUR_GCS_BUCKET"
GOOGLE_CLOUD_VISION_API_KEY = "REPLACE_ON_DEPLOYMENT-129dc531-ad4a-430f-aa1e-1b241f5435d1"

ADMIN_API_KEY = "REPLACE_ON_DEPLOYMENT-1e3db3d0-59d0-4e13-aafe-cc228e527c90"

SEARCH_INDEX = "restaurant_search_v1"


try:
    from local_settings import *
except ImportError:
    pass

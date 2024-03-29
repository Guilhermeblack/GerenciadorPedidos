"""
Django settings for Atendgb project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import cloudinary  # cloudinary
import cloudinary.uploader  # cloudinary
import cloudinary.api  # cloudinary
import cloudinary.api  # cloudinar
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '14ns^8=os!q@q(m@wo&1nqo42o_*q*fh3=l$hx!i(#x--@wh4y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_ajax',
    'pwa',
    'Atendgb',
    'gerenciador',
    'cloudinary',
    'channels'
    # 'django_pagarme',
    # 'django_signal_notifier',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'Atendgb.urls'

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


WSGI_APPLICATION = 'Atendgb.wsgi.application'
ASGI_APPLICATION  = 'Atendgb.asgi.application'

REDIS_URL = 'redis://:JgnO7QjePRVCxKxdqoR713Nlu49VNKMy@redis-13847.c1.us-central1-2.gce.cloud.redislabs.com:13847'


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CHANNEL_LAYERS = {
    'default': {
        ## Method 1: Via redis lab
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [
              REDIS_URL

            ],
        },

        ### Method 2: Via local Redis
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #      "hosts": [('redis', 6379),('127.0.0.1', 6379)],
        # },

        ### Method 3: Via In-memory channel layer
        ## Using this method.
        # "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}


LOGOUT_REDIRECT_URL = '/'

LOGIN_URL = '/loguin'

LOGIN_REDIRECT_URL = '/profile'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedSHA1PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
]



STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/pt/2.2/howto/static-files/




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd8aa7cgop6qt0i',
        'USER': 'hezvwzayygpuor',
        'PASSWORD': '800bd5a88f41d5a5266e22316667b536b22153f19c7dce9fdeb3bf7645393d34',
        'HOST': 'ec2-44-207-30-235.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}

import dj_database_url
# DATABASES['default'] = dj_database_url.config(default='postgres://hezvwzayygpuor:800bd5a88f41d5a5266e22316667b536b22153f19c7dce9fdeb3bf7645393d34@ec2-44-207-30-235.compute-1.amazonaws.com:5432/d8aa7cgop6qt0i')


# essa linha
# DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO','https')




STATIC_URL = '/static/'
MEDIA_URL = '/media/'


STATICFILES_DIRS = ( os.path.join(BASE_DIR, '/static'), )
MEDIA_ROOT = os.path.join(BASE_DIR, '../GerenciadorPedidos/gerenciador/static')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, '../GerenciadorPedidos/gerenciador/')





# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../GerenciadorPedidos/gerenciador/static'),
)

PWA_APP_NAME = 'Gerenciador-GBlack'
PWA_APP_DESCRIPTION = "gerenciador de pedidos e comandas para estabelecimentos comerciais"
PWA_APP_THEME_COLOR = '#0A0302'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/images/my_app_icon.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/my_apple_icon.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icons/splash-640x1136.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'pt-BR'


cloudinary.config(
    cloud_name="gblack",
    api_key="191418815964556",
    api_secret="hvTxhjD4ZyfYigVrte6ucol0lio"
)

# Dados para integração com Pagarme
CHAVE_PAGARME_API_PRIVADA = 'ak_live_8jUYbLG5ojzgs9wisry243ycehrk1g'
CHAVE_PAGARME_CRIPTOGRAFIA_PUBLICA = 'ek_live_kwLtZhdUxIWxbGGC4cHq7cddKh5T21'

# Para validar telefones no Brasil
PHONENUMBER_DEFAULT_REGION = 'BR'


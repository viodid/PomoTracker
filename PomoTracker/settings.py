"""
Django settings for PomoTracker project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print('Base dir: ', BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

DEBUG = bool(os.environ.get('DJANGO_DEBUG', False))
SECRET_KEY = 'django-instance-secret-key' if DEBUG else os.environ.get("SECRET_KEY")
CSRF_COOKIE_SECURE              = True
SESSION_COOKIE_SECURE           = True
SECURE_SSL_REDIRECT             = True
SECURE_HSTS_PRELOAD             = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 3600
DEBUG_PROPAGATE_EXCEPTIONS      = True
SERVER_EMAIL                    = "webmaster@pomotracker.app"
ALLOWED_HOSTS                   = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
CSRF_TRUSTED_ORIGINS            = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS").split(" ")



print('DEBUG: ', DEBUG,
    '\nDJANGO_SECURE_SSL_REDIRECT: ', SECURE_SSL_REDIRECT,
    '\nDEBUG_PROPAGATE_EXCEPTIONS: ', DEBUG_PROPAGATE_EXCEPTIONS,
    '\nALLOWED_HOSTS' , ALLOWED_HOSTS,
    '\nCSRF_TRUSTED_ORIGINS: ', CSRF_TRUSTED_ORIGINS,)


# Application definition

INSTALLED_APPS = [
    'app',
    'api',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

# Allauth settings
SITE_ID                         = 2
ACCOUNT_EMAIL_REQUIRED          = False
ACCOUNT_EMAIL_VERIFICATION      = False
ACCOUNT_SESSION_REMEMBER        = True
ACCOUNT_AUTHENTICATION_METHOD   = 'username'
ACCOUNT_USERNAME_REQUIRED       = True
ACCOUNT_USER_MODEL_EMAIL_FIELD  = None
ACCOUNT_LOGIN_ATTEMPTS_LIMIT    = 10
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT  = 1800
ACCOUNT_PASSWORD_MIN_LENGTH     = 12
ACCOUNT_DEFAULT_HTTP_PROTOCOL   = "https"
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False
SOCIALACCOUNT_AUTO_SIGNUP       = True
LOGIN_REDIRECT_URL              = '/'
LOGOUT_REDIRECT_URL             = '/'
ACCOUNT_SIGNUP_REDIRECT_URL     = '/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PomoTracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'app/templates', 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # https://stackoverflow.com/questions/2223429/django-global-template-variables
                'app.context_processors.global_settings',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # used for default signin such as loggin into admin panel
    'django.contrib.auth.backends.ModelBackend',

    # used for social authentications
    'allauth.account.auth_backends.AuthenticationBackend',
)

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

WSGI_APPLICATION = 'PomoTracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# https://docs.djangoproject.com/en/4.2/ref/databases/#persistent-database-connections

CONN_MAX_AGE = 0

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME_TEST") if DEBUG else os.environ.get("DB_NAME_TEST"), # ESTA LINEA ME HA COSTADO 3 DIAS DEBUGGEANDO
        'USER': os.environ.get("DB_USER"),
        'HOST': os.environ.get("DB_HOST_PUBLIC") if DEBUG else os.environ.get("DB_HOST_PRIVATE"), # TODO: change to DB_HOST_PRO
        'PORT': os.environ.get("DB_PORT"),
        'PASSWORD': os.environ.get("DB_USER_PASSWORD")
    }
}

print('DATABASE_HOST: ',DATABASES['default']['HOST'])

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{os.environ.get('REDIS_HOST')}:6379",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_TZ = True

TIME_ZONE = 'UTC'

USE_I18N = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# STATIC_URL is the base URL prefix for generating URLs to your static
# files in your templates and code.
# STATIC_ROOT is the absolute filesystem path where collected static files
# are stored for production serving.

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/4.2/ref/settings/#media-root

#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MEDIA_URL = 'media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

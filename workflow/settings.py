#!/usr/bin/env python
#-*- coding: utf-8 -*-#  Copyright 2013 Findspire

''' Django settings for findspire project '''

import os
import os.path
import sys

DEBUG = True

HAMLPY_ATTR_WRAPPER = '"'
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = os.getcwd() + '/static'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.getcwd() + '/workflow/static']
ALLOWED_HOSTS = ['*']
USE_X_FORWARDED_HOST = True
TIME_ZONE = 'UTC'
APPEND_SLASH = True
SITE_ID = 1
ADMINS = ()
MANAGERS = ADMINS
LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', 'English'),
    ('fr', 'Francais'),
)
AVAILABLE_LANGUAGES = dict(LANGUAGES).keys()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.dirname(__file__) + '/../workflow.db',
    }
}

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

CACHES = {
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    # }
}

#AUTHENTICATION_BACKENDS = (
#    'workflow.auth.AuthBackend',
#)

#SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = REDIS_HOST
SESSION_REDIS_PORT = REDIS_PORT
SESSION_REDIS_PREFIX = 'sessionweb'
SESSION_COOKIE_AGE = 2*7*86400
SESSION_COOKIE_SECURE = False
PROFILE_COOKIE_SECURE = False

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '6og(!94ejbbv6x($=gn&amp;x3ea9ffb!64ev4%3jv(m*uy8-0@f=5'

#### TEMPLATE STUFF ####

TEMPLATE_LOADERS = (
    'hamlpy.template.loaders.HamlPyFilesystemLoader',
    'hamlpy.template.loaders.HamlPyAppDirectoriesLoader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_DEBUG = DEBUG

TEMPLATE_DIRS = (os.getcwd() + '/workflow/templates/')
print TEMPLATE_DIRS



MIDDLEWARE_CLASSES = (
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

DOMAIN = 'findspire.com'
ROOT_URLCONF = 'workflow.urls'

WSGI_APPLICATION = 'workflow.wsgi.application'

INSTALLED_APPS = (
    'django_user_agents',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'south',
    'workflow.apps.workflow',
    'rest_framework',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(levelname).4s] %(message)s - %(pathname)s:%(lineno)s',
            'datefmt': '%H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# change this to true to enable logging to the console.
LOG_TO_CONSOLE = True

if LOG_TO_CONSOLE:
    LOGGING['loggers'][''] = {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': True,
    }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'EXCEPTION_HANDLER': 'workflow.apps.restws.response.exception_handler',
}


# Overwrite this in local_settings.py
BASICAUTH_USERS = {
    #"username": "password"
}

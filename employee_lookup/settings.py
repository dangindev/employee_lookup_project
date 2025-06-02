import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'django_extensions',
    
    # Local apps
    'authentication',
    'employees',
    'companies',
    'core',
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

ROOT_URLCONF = 'employee_lookup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'employee_lookup.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
    }
}

# Password validation
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
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'authentication.CustomUser'

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Login/Logout URLs
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/auth/login/'

# LDAP Configuration từ .env
LDAP_ENABLED = config('LDAP_ENABLED', default=True, cast=bool)

if LDAP_ENABLED:
    import ldap
    from django_auth_ldap.config import LDAPSearch, ActiveDirectoryGroupType
    
    # LDAP Server Settings
    AUTH_LDAP_SERVER_URI = config('LDAP_SERVER_URI', default='')
    AUTH_LDAP_BIND_DN = config('LDAP_BIND_DN', default='')
    AUTH_LDAP_BIND_PASSWORD = config('LDAP_BIND_PASSWORD', default='')
    
    # User Search
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        config('LDAP_USER_SEARCH_BASE', default=''),
        ldap.SCOPE_SUBTREE,
        config('LDAP_USER_SEARCH_FILTER', default='(sAMAccountName=%(user)s)')
    )
    
    # Group Settings
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        config('LDAP_GROUP_SEARCH_BASE', default=''),
        ldap.SCOPE_SUBTREE,
        config('LDAP_GROUP_SEARCH_FILTER', default='(objectClass=group)')
    )
    AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType()
    
    # User Attribute Mapping
    AUTH_LDAP_USER_ATTR_MAP = {
        "first_name": config('LDAP_ATTR_FIRST_NAME', default='givenName'),
        "last_name": config('LDAP_ATTR_LAST_NAME', default='sn'),
        "email": config('LDAP_ATTR_EMAIL', default='mail'),
    }
    
    # User Flags
    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        "is_active": f"CN=Domain Users,CN=Users,{config('LDAP_GROUP_SEARCH_BASE', default='')}",
    }
    
    # Always update user from LDAP
    AUTH_LDAP_ALWAYS_UPDATE_USER = config('LDAP_ALWAYS_UPDATE_USER', default=True, cast=bool)
    
    # Cache settings
    AUTH_LDAP_CACHE_TIMEOUT = config('LDAP_CACHE_TIMEOUT', default=3600, cast=int)
    
    # Global options for LDAP
    AUTH_LDAP_CONNECTION_OPTIONS = {
        ldap.OPT_REFERRALS: 0,
        ldap.OPT_DEBUG_LEVEL: 0,
        ldap.OPT_NETWORK_TIMEOUT: config('LDAP_CONNECTION_TIMEOUT', default=10, cast=int),
    }
    
    # Authentication backends với LDAP
    AUTHENTICATION_BACKENDS = [
        'authentication.backends.CustomLDAPBackend',
        'authentication.backends.SystemAccountBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]
else:
    # Authentication backends không có LDAP
    AUTHENTICATION_BACKENDS = [
        'authentication.backends.SystemAccountBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]

# Session settings
SESSION_COOKIE_AGE = 8 * 60 * 60  # 8 hours
SESSION_SAVE_EVERY_REQUEST = True

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django_auth_ldap': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },
        'employees': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Tạo thư mục logs
import os
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

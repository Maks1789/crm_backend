import os
from pathlib import Path
from dotenv import load_dotenv # Імпортуємо функцію для завантаження .env файлу

# Завантажуємо змінні з .env файлу
# Переконайтеся, що файл .env знаходиться в кореневій директорії вашого проєкту
# (там, де лежить manage.py).
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- General Django Settings from .env ---
# SECURITY WARNING: keep the secret key used in production secret!
# Отримуємо SECRET_KEY з .env. Якщо його немає, додаток не запуститься (це добре для безпеки).
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set!")


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG буде True, якщо в .env DEBUG=True або якщо змінної немає
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# ALLOWED_HOSTS з .env, розділені комами
ALLOWED_HOSTS = [host.strip() for host in os.environ.get('ALLOWED_HOSTS', '').split(',') if host.strip()]
if DEBUG: # Дозволяємо localhost для DEBUG режиму, незалежно від .env
    ALLOWED_HOSTS.append('localhost')
    ALLOWED_HOSTS.append('127.0.0.1')
    ALLOWED_HOSTS.append('[::1]') # Для IPv6

# Налаштування CSRF
# Вказує, звідки дозволено надсилати CSRF-токен.
CSRF_TRUSTED_ORIGINS = [
    'http://213.111.120.85',
    'https://213.111.120.85',
    'http://localhost:80',
    # Якщо ви використовуєте HTTPS, додайте і його
    # 'https://your_domain.com'
]

# Налаштування CORS
# Встановіть список дозволених доменів для крос-доменних запитів.
# Зазвичай це домен вашого фронтенду.
CORS_ALLOWED_ORIGINS = [
    'http://213.111.120.85',
    'https://213.111.120.85',
    'http://localhost:80',
]



# --- CORS Settings (if you use django-cors-headers) ---
# Розкоментуйте, якщо ви використовуєте бібліотеку django-cors-headers
# INSTALLED_APPS += ['corsheaders']
# MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware') # Важливо: має бути на початку
# CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
# CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'False').lower() == 'true'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'testter',
    'rest_framework',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'testter.log_middleware.RequestHeadersLoggingMiddleware',
]
OTP_TOTP_ISSUER = 'mini_crm_sistem'

ROOT_URLCONF = 'testBack.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'testBack.wsgi.application'


# --- Database Settings from .env ---
# Отримуємо налаштування бази даних з .env файлу
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),         # Ім'я бази даних
        'USER': os.environ.get('POSTGRES_USER'),         # Ім'я користувача бази даних
        'PASSWORD': os.environ.get('DB_PASSWORD'), # Пароль користувача бази даних
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),

    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'uk') # Мова з .env
TIME_ZONE = os.environ.get('TIME_ZONE', 'Europe/Kyiv') # Часова зона з .env

USE_I18N = os.environ.get('USE_I18N', 'True').lower() == 'true'
USE_TZ = os.environ.get('USE_TZ', 'True').lower() == 'true'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'  #os.environ.get('STATIC_URL', 'static/')
STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT', 'staticfiles') # BASE_DIR / 'staticfiles' # Місце, куди Django збиратиме статичні файли для продакшену
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = os.environ.get('MEDIA_URL', 'media/') # Додайте для медіафайлів
MEDIA_ROOT =  BASE_DIR / 'mediafiles' # Місце, куди завантажуватимуться медіафайли 'mediafiles'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Використовувати стиснену та контрольовану WhiteNoise сховище


# --- Security Settings (for production, use with HTTPS) ---
# Розкоментуйте та налаштуйте для продакшену, якщо використовуєте HTTPS
# SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
# SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
# CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'False').lower() == 'true'
# SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 0))
# CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')





# """
# Django settings for testBack project.
#
# Generated by 'django-admin startproject' using Django 5.2.2.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/5.2/topics/settings/
#
# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/5.2/ref/settings/
# """
#
# from pathlib import Path
#
# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
#
#
# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
#
# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-x0n+*9x5c9y^*h3#()ds20irpx@ne4^pafy-o#iv3%so33@cu@'
#
# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# CORS_ALLOW_ALL_ORIGINS = True
# # ALLOWED_HOSTS = ['*']
# #
# # CORS_ALLOW_ALL_ORIGINS = True
# #
# # CORS_ALLOWED_ORIGINS = [
# #     "http://localhost:5173",
# # ]
#
# # Application definition
#
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'testter',
#     'rest_framework',
# ]
#
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',          # <-- Зверніть увагу на порядок
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',       # <-- Зверніть увагу на порядок
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     # 'corsheaders.middleware.CorsMiddleware', # Якщо використовуєте django-cors-headers, то тут
#     'testter.log_middleware.RequestHeadersLoggingMiddleware', # <-- Ваш middleware ТУТ
# ]
#
#
#
# ROOT_URLCONF = 'testBack.urls'
#
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]
#
# WSGI_APPLICATION = 'testBack.wsgi.application'
#
#
# # Database
# # https://docs.djangoproject.com/en/5.2/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
#
#
# # Password validation
# # https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
#
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]
#
#
# # Internationalization
# # https://docs.djangoproject.com/en/5.2/topics/i18n/
#
# LANGUAGE_CODE = 'uk'
#
# TIME_ZONE = 'Europe/Kiev'
#
# USE_I18N = True
#
# USE_TZ = True
#
#
# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/5.2/howto/static-files/
#
# STATIC_URL = 'static/'
#
# # Default primary key field type
# # https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
#
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

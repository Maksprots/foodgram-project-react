import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    default='8gmelpy0)8icp0##o(0#xy8#19p7ma6v4+pbnc)gsc3k64l!ce')

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djoser',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'api.apps.ApiConfig',
    'users.apps.UsersConfig',
    'recipes.apps.RecipesConfig',
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

ROOT_URLCONF = 'foodgram.urls'

TEMPLATES_DIR = BASE_DIR / 'docs'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'foodgram.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', default='postgres'),
        'USER': os.getenv('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
        'HOST': os.getenv('DB_HOST', default='db'),
        'PORT': os.getenv('DB_PORT', default='5432')
    }
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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 6,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
}

DJOSER = {
    'HIDE_USERS': False,
    'LOGIN_FIELD': 'email',
}

MAX_LEN_USER_EMAIL = 256
MAX_LEN_USER_FIELD = 150
EMPTY_VALUE_DISPLAY = '-empty-'
EMPTY_CART = 'В корзине нет товаров'
SHOPPING_LIST = 'Список покупок:'
ERROR_FOLLOW_AUTHOR = 'Вы не были подписаны на автора'
ERROR_FAVORITE_RECIPE = 'Рецепт не в избранном'
ERROR_RECIPE_DOESNT_CART = 'Рецепта нет в корзине'
ERROR_TAG = 'Ошибка в Тэге, id = {pk_value} не существует'
MIN_LEN_NAME_RECIPE = 'Название рецепта минимум 4 символа'
ERROR_INGREDIENT_ID = 'Ингредиента с id - {ingredient} нет'
ERROR_INGREDIENTS_REPEAT = 'Ингредиенты не должны повторяться!'
ERROR_TAG_REPEAT = 'Тэги не должны повторяться!'
MIN_AMOUNT_OF_INGREDIENT = 'Минимальное количество ингридиента 1'
INTERVAL_OF_COOKING = 'Время приготовления блюда от 1 до 300 минут'
ERROR_EQUAL_PASSWORD = "Пароли не должны совпадать"
ERROR_WRONG_PASSWORD = "Введен неверный пароль"
ERROR_FOLLOW_YOUSELF = 'Нельзя подписаться на самого себя'
ERROR_ALREADY_FOLLOW = 'Вы уже подписаны на данного пользователя'
RECIPE_ALREADY_IN_FAVORITE = 'Рецепт уже в избранном'
RECIPE_ALREADY_IN_SHOPLIST = 'Рецепт уже добавлен в список покупок'

# plant_diseases/settings.py

from pathlib import Path
import os # os module import করা হয়েছে

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e#7y2b78q1o*y#3k*9n31x%*y0o@2m#&_&c-0t2s^w9-q-i&c9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # ডেভেলপমেন্টের জন্য True রাখা হয়েছে

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # এটি যোগ করুন
    'weathernews',    # এটি যোগ করুন
    'detector',       # যদি detector অ্যাপটি আপনার প্রোজেক্টে থাকে
    'agrinews',       # যদি agrinews অ্যাপটি আপনার প্রোজেক্টে থাকে
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

ROOT_URLCONF = 'plant_diseases.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # এখানে আপনার মূল টেমপ্লেট ডিরেক্টরি যোগ করুন
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

WSGI_APPLICATION = 'plant_diseases.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka' # বাংলাদেশের সময় অঞ্চল সেট করা হয়েছে

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Gemini API Key (প্রোডাকশনে এনভায়রনমেন্ট ভেরিয়েবল থেকে লোড করুন!)
# DEVELOPMENT_ONLY_GEMINI_API_KEY = "AIzaSyAiqY4TORhOhbhPYrLzTWdeDxEJwqG3ZOQ" # এই লাইনটি মুছে ফেলা হয়েছে বা কমেন্ট করা হয়েছে

# আপনার পরিবেশ পরিবর্তনশীল থেকে লোড করা উচিত:
# os.getenv() ব্যবহার করা হয়েছে। আপনি আপনার পরিবেশ ভেরিয়েবল 'GEMINI_API_KEY' সেট করতে ভুলবেন না।
# ডেভেলপমেন্টের সুবিধার জন্য, একটি ফলব্যাক হিসাবে আপনি সরাসরি এখানে একটি কী দিতে পারেন,
# তবে প্রোডাকশনে এটি **কখনও** করবেন না।
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCz5GNe5tFuyICMfP-iKAnFXy6zPSi1feA")
GEMINI_MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
"""
Django settings for autoplatform project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR,'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@2tfo$i&ki($)3e5hgp5x4r&savw3$l=m!qosmxc6#b3=ghrh&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'corsheaders',  #解决跨域的问题，前端项目启动后需要跨域请求前后端需要填写一样地址和端口，尽量放到第一个
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'projects.apps.ProjectsConfig', # 添加子应用，但不能添加在rest_framework后面
    'interfaces.apps.InterfacesConfig',# 添加子应用，但不能添加在rest_framework后面
    'user.apps.UserConfig',
    'configures.apps.ConfiguresConfig',
    'testcases.apps.TestcasesConfig',
    'envs.apps.EnvsConfig',
    'testsuits.apps.TestsuitsConfig',
    'debugtalks.apps.DebugtalksConfig',
    'reports.apps.ReportsConfig',
    'django_filters',
    'rest_framework'   #pip install djangprestframwork 安装后需要在此添加
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware', #解决跨域问题，需要放在django.contrib.sessions.middleware.SessionMiddleware的上面
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#添加白名单
#CORS_ORIGIN_ALLOW_ALL = True,表示所有域名(ip)都可以访问后端接口，默认为false
CORS_ORIGIN_ALLOW_ALL = True


'''
CORS_ORIGIN_WHITELIST表示指定能够访问后端接口的ip或域名列表
'''
# CORS_ORIGIN_WHITELIST = [
#     'http://127.0.0.1:8080',
#     'http://192.168.1.63:8080'
# ]


ROOT_URLCONF = 'autoplatform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'autoplatform.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dev04',
        'HOST': 'localhost',
        'PORT': "3306",
        'USER': 'root',
        'PASSWORD': '111111'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY':'errors',
    #指定全局的过滤引擎
    'DEFAULT_FILTER_BACKENDS':['django_filters.rest_framework.backends.DjangoFilterBackend'],
    #指定分页引擎
   # 'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',

    'DEFAULT_PAGINATION_CLASS':'utils.pagination.MyPagination',
    #必须指定每页每页的数据条数
    #'PAGE_SIZE':3,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # DEFAULT_AUTHENTICATION_CLASSES指定默认的认证类（认证方式）
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 会话认证
        'rest_framework.authentication.SessionAuthentication',
        # 基本认证（用户名和密码认证）
        'rest_framework.authentication.BasicAuthentication',
        #指定使用JWT token认证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication'
    ],
}

# 可以在全局配置settings.py中的LOGGING，来配置日志信息
LOGGING = {
    # 版本号
    'version': 1,
    # 指定是否禁用已经存在的日志器
    'disable_existing_loggers': False,
    # 日志的显示格式
    'formatters': {
        # simple为简化版格式的日志
        'simple': {
            'format': '%(asctime)s - [%(levelname)s] - [msg]%(message)s'
        },
        # verbose为详细格式的日志
        'verbose': {
            'format': '%(asctime)s - [%(levelname)s] - %(name)s - [msg]%(message)s - [%(filename)s:%(lineno)d ]'
        },
    },
    # filters指定日志过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # handlers指定日志输出渠道
    'handlers': {
        # console指定输出到控制台
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # 日志保存到日志文件
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            # 指定存放日志文件的所处路径
            'filename': os.path.join(BASE_DIR, "logs/test.log"),  # 日志文件的位置
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
    },
    # 定义日志器
    'loggers': {
        'log': {  # 定义了一个名为mytest的日志器
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'DEBUG',  # 日志器接收的最低日志级别
        },
    }
}


'''
前段用户访问认证之后的接口，需要在请求头携带参数：
Authorization为key，值为JWT + 空格 + token值，如 Authorization: JWT xxxxxxxxxxxxxxx
'''
JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'utils.jwt_handle.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1) #  指定token过期时间
}
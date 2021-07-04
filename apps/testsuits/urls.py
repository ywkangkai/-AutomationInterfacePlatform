
from django.urls import path, re_path

from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views


# 定义路由对象
router = SimpleRouter()
router.register(r'testsuits', views.TestsuitsViewSet)

urlpatterns = []
urlpatterns += router.urls

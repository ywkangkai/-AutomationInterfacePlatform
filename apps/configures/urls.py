
from rest_framework.routers import SimpleRouter

from . import views


# 定义路由对象
router = SimpleRouter()
router.register(r'configures', views.ConfiguresViewSet)

urlpatterns = [

]
urlpatterns += router.urls

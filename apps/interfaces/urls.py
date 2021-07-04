
from rest_framework.routers import SimpleRouter

from . import views


# 定义路由对象
router = SimpleRouter()
router.register(r'interfaces', views.InterfacesViewSet)

urlpatterns = [

]
urlpatterns += router.urls

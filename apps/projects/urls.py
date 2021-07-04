
from django.urls import path, re_path

from rest_framework.routers import DefaultRouter, SimpleRouter

# from projects.views import
from projects import views


# 定义路由对象
# router = SimpleRouter()
# DefaultRouter相比SimpleRouter，自动添加了一条根路径的路由 /  -> 可浏览器的api页面
router = DefaultRouter()
# 使用路由对象.register()方法，来进行注册
# a.第一个参数指定路由前缀，r'子应用名小写'
# b.第二个参数指定视图集类即可，不要调用.as_view()
router.register(r'projects', views.ProjectsViewSet)

urlpatterns = [
    # path('projects/', views.ProjectsView.as_view()),
    # path('projects/<int:pk>/', views.ProjectDetailView.as_view()),

    # a.继承ViewSet之后，支持在定义路由时指定请求方法与action的映射
    # b.as_view需要接收一个字典
    # c.key为请求方法名，value为指定需要调用的action
    # path('projects/', views.ProjectsViewSet.as_view({
    #     'get': 'list',
    #     'post': 'create'
    # })),
    # path('projects/names/', views.ProjectsViewSet.as_view({
    #     'get': 'names'
    # })),
    # path('projects/<int:pk>/', views.ProjectsViewSet.as_view({
    #     'get': 'retrieve',
    #     'put': 'update',
    #     'delete': 'destroy'
    # })),
    # path('projects/<int:pk>/interfaces/', views.ProjectsViewSet.as_view({
    #     'get': 'interfaces'
    # })),
]

# 使用路由对象.urls属性来获取自动生成的路由条目，往往为列表
# 需要将这个列表添加至urlpatterns
urlpatterns += router.urls


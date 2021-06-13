from django.urls import path, re_path

# from projects.views import
from projects import views

'''
需要集成ViewSet才能使用这种写法，
使用映射关系，根据不通的路径去找不通的方法
'''
urlpatterns = [
    path('projects/', views.ProjectViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('projects/<int:pk>/', views.ProjectViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),

]

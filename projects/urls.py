from django.urls import path, re_path

# from projects.views import
from projects import views

'''
需要集成ViewSet才能使用这种写法，
使用映射关系，根据不通的路径去找不通的方法
'''
urlpatterns = [
    path('projects/', views.ProjectsViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('projects/names', views.ProjectsViewSet.as_view({
        'get': 'names',
    })),
    path('projects/<int:pk>/', views.ProjectsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('projects/<int:pk>/interfaces', views.ProjectsViewSet.as_view({
        'get': 'interfaces',
    })),
]

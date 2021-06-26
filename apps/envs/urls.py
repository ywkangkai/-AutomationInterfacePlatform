from django.urls import path, re_path

from envs import views


urlpatterns = [
    path('envs/', views.EnvsViewSet.as_view({
        'get': 'list',
        'post':'create'
    })),
    path('envs/<int:pk>/', views.EnvsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('envs/names/', views.EnvsViewSet.as_view({
        'get': 'names',
    })),

]

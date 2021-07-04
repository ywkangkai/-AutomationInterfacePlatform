from django.urls import path, re_path

from interfaces import views


urlpatterns = [
    path('testsuits/', views.InterfacesViewSet.as_view({
        'get': 'list',
        'post':'create'
    })),
    path('testsuits/<int:pk>/', views.InterfacesViewSet.as_view({
        'put': 'update',
        'get':'retrieve'
    })),

]

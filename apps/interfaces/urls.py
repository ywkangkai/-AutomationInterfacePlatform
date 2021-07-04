from django.urls import path, re_path

from interfaces import views


urlpatterns = [
    path('interfaces/', views.InterfacesViewSet.as_view({
        'post': 'create',
        'get': 'list'
    })),
    path('interfaces/<int:pk>', views.InterfacesViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
]

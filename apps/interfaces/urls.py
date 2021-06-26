from django.urls import path, re_path

from interfaces import views


urlpatterns = [
    path('interfaces/', views.InterfacesViewSet.as_view({
        'post': 'create',
        'get': 'list'
    })),


]

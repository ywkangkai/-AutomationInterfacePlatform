from django.urls import path, re_path

from reports import views


urlpatterns = [
    path('reports/', views.ReportsViewSet.as_view({
        'get': 'list'
    })),
    path('testsuits/<int:pk>/', views.ReportsViewSet.as_view({
        'put': 'update',
        'get':'retrieve'
    })),

]

from django.urls import path, re_path

from interfaces import views


urlpatterns = [
    path('interfaces/', views.InterfacesView.as_view()),
    #path('projects/<int:pk>/', views.ProjectDetailView.as_view()),

]

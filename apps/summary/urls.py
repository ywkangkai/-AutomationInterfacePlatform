from django.urls import path
from rest_framework import routers

from .views import SummaryAPIView


urlpatterns = [
    path('summary/', SummaryAPIView.as_view()),
]

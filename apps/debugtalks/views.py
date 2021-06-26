import logging
from django.db.models import Q, Count
from interfaces.models import Interfaces
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import DebugTalksModelSerializer


logger = logging.getLogger('log')  #这里的log是setting中189行自己定义的名字



class InterfacesViewSet(viewsets.ModelViewSet):
    queryset = Interfaces.objects.all()
    serializer_class = DebugTalksModelSerializer











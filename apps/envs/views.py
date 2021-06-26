import logging
from django.db.models import Q, Count
from envs.models import Envs
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import EnvsModelSerializer,EnvsNamesSerializer
from rest_framework.filters import OrderingFilter

logger = logging.getLogger('log')  #这里的log是setting中189行自己定义的名字



class EnvsViewSet(viewsets.ModelViewSet):
    queryset = Envs.objects.all()
    serializer_class = EnvsModelSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['id','name']


    def get_serializer_class(self):
        if self.action == 'names':
            return EnvsNamesSerializer
        else:
            return self.serializer_class


    @action(methods=['get'],detail=False)
    def names(self,request):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        serializer_obj = self.get_serializer(instance=qs,many=True)
        return Response(serializer_obj.data)





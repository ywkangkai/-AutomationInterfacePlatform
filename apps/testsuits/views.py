import logging
from testsuits.models import Testsuits
from rest_framework import viewsets
from .serializers import TestsuitsModelSerializer
from rest_framework.response import Response

logger = logging.getLogger('log')  #这里的log是setting中189行自己定义的名字



class InterfacesViewSet(viewsets.ModelViewSet):
    queryset = Testsuits.objects.all()
    serializer_class = TestsuitsModelSerializer


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {
            'name':instance.name,
            'project_id': instance.project_id,
            'include': instance.include
        }
        return Response(data)




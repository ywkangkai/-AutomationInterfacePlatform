from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Testsuits
from .serializers import TestsuitsModelSerializer


class TestsuitsViewSet(ModelViewSet):
    queryset = Testsuits.objects.all()
    serializer_class = TestsuitsModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['id', 'name']

    # def get_serializer_class(self):
    #     # if self.action == 'names':
    #     #     return EnvsNamesSerializer
    #     # else:
    #     #     return self.permission_classes
    #     return EnvsNamesSerializer if self.action == 'names' else self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {
            'name': instance.name,
            'project_id': instance.project_id,
            'include': instance.include
        }
        return Response(data)

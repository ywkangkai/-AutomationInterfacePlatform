from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Envs
from .serializers import EnvsModelSerializer, EnvsNamesSerializer


class EnvsViewSet(ModelViewSet):
    queryset = Envs.objects.all()
    serializer_class = EnvsModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['id', 'name']

    @action(detail=False)
    def names(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        # if self.action == 'names':
        #     return EnvsNamesSerializer
        # else:
        #     return self.permission_classes
        return EnvsNamesSerializer if self.action == 'names' else self.serializer_class

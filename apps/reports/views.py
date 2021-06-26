import logging
from reports.models import Reports
from rest_framework import viewsets
from .serializers import ReportsModelSerializer
from rest_framework.response import Response

logger = logging.getLogger('log')  #这里的log是setting中189行自己定义的名字



class ReportsViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsModelSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)







import json
import logging

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

# from rest_framework import filters
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
import json
from .models import Testcases
from .serializers import TestcasesModelSerializer

# from utils.pagination import MyPagination
# 定义日志器用于记录日志，logging.getLogger('全局配置settings.py中定义的日志器名')
logger = logging.getLogger('mytest')


class TestcasesViewSet(viewsets.ModelViewSet):


    queryset = Testcases.objects.all()
    serializer_class = TestcasesModelSerializer

    def retrieve(self, request, *args, **kwargs):
        testcase_obj = self.get_object()
        #获取用例前置信息
        testcase_include = json.loads(testcase_obj.include,encoding='utf-8')
        print(testcase_include)
        return testcase_include


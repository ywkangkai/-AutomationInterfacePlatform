import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render #用于返回html页面 重定向
from django.db.models import Q, Count #组合查询
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from .models import Projects
from rest_framework import viewsets
from rest_framework.response import Response #需要结合APIview使用
from .serializers import ProjectsModelSerializer
from django_filters.rest_framework import DjangoFilterBackend  #pip install django_filters
from rest_framework.filters import OrderingFilter #指定排序引擎


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()  # 需要指定queryset，当前接口中需要使用到的查询集
    serializer_class = ProjectsModelSerializer  # 需要指定serializer_class，当前接口中需要使用到的序列化器类
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # DRF框架中的过滤引擎，有它才能对下面字段进行过滤
    filterset_fields = ['name', 'leader']  # 可根据这些字段进行过滤，任意添加模型类中的字段
    ordering_fields = ['name', 'leader', 'id']  # 可根据这些字段进行排序，任意添加模型类中的字段


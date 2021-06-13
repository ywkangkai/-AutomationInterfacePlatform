import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render #用于返回html页面 重定向
from django.db.models import Q, Count #组合查询
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from .models import Projects
from rest_framework.response import Response #需要结合APIview使用
from .serializers import ProjectsModelSerializer
from django_filters.rest_framework import DjangoFilterBackend  #pip install django_filters
from rest_framework.filters import OrderingFilter #指定排序引擎


#mixins需要与GenericAPIView联合继承使用，需要用到GenericAPIView的queryset与serializer_class
class ProjectsView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   GenericAPIView):#如果要实现过滤，查询，分页等功能，需要继承GenericAPIView

    queryset = Projects.objects.all() #需要指定queryset，当前接口中需要使用到的查询集
    serializer_class = ProjectsModelSerializer #需要指定serializer_class，当前接口中需要使用到的序列化器类
    filter_backends = [DjangoFilterBackend,OrderingFilter] #DRF框架中的过滤引擎，有它才能对下面字段进行过滤
    filterset_fields = ['name','leader'] #可根据这些字段进行过滤，任意添加模型类中的字段
    ordering_fields = ['name','leader','id'] #可根据这些字段进行排序，任意添加模型类中的字段


    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs) #mixins.ListModelMixin下有一个list方法，做了分页查询的功能

    def post(self, request, *args, **kwargs):

       return self.create(request, *args, **kwargs) #mixins.CreateModelMixin下有一个create方法，封装了create方法


class ProjectDetailView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        GenericAPIView):

    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer

    def get(self, request, *args, **kwargs):

        return self.retrieve(request, *args, **kwargs) #mixins.RetrieveModelMixin下有一个retrieve方法，实现了单个查询

    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs) #mixins.UpdateModelMixin下有一个update方法，实现更改数据的功能

    def delete(self, request, *args, **kwargs):

        return self.delete(request, *args, **kwargs) #mixins.DestroyModelMixin下有一个delete方法，实现删除数据的功能




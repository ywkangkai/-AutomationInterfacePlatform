import logging
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render  # 用于返回html页面 重定向
from django.db.models import Q, Count  # 组合查询
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from .models import Projects
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response  # 需要结合APIview使用
from .serializers import ProjectsModelSerializer, InterfacesByProjectsNameModelSerializer,ProjectsNamesModelSerializer
from django_filters.rest_framework import DjangoFilterBackend  # pip install django_filters
from rest_framework.filters import OrderingFilter  # 指定排序引擎

'''
1.ModelViewSet他继承了mixins中的增删查改与GenericViewSet，
    class ModelViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):

2.根据URL中的映射关系实现了自动调用增删查改对应的接口方法

3.搞清GenericViewSet的作用（分页，过滤），搞清mixins简化增删查改的写法

搞清几个概念：
    get—list：就是在做查询，这里查询大量数据对他们进行分页（要分页前提就需要GenericViewSet中的queryset与serializer_class），mixins.ListModelMixin下有一个list方法
    get—retrieve：也是查询，但是是查看单条数据详情，mixins.RetrieveModelMixin下有一个retrieve方法
    post—create：创建数据接口，mixins.CreateModelMixin下有一个create方法
    put—update：修改接口，mixins.UpdateModelMixin下有一个update方法
    delete—destroy，删除接口，mixins.DestroyModelMixin下有一个destroy
'''

logger = logging.getLogger('log')  #这里的log是setting中189行自己定义的名字

class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()  # 需要指定queryset，当前接口中需要使用到的查询集
    serializer_class = ProjectsModelSerializer  # 需要指定serializer_class，当前接口中需要使用到的序列化器类
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # DRF框架中的过滤引擎，有它才能对下面字段进行过滤
    filterset_fields = ['name', 'leader']  # 可根据这些字段进行过滤，任意添加模型类中的字段
    ordering_fields = ['name', 'leader', 'id']  # 可根据这些字段进行排序，任意添加模型类中的字段

    # 重写父类的get_serializer_class
    def get_serializer_class(self):
        if self.action == 'names':
            return ProjectsNamesModelSerializer
        elif self.action == 'interfaces':
            return InterfacesByProjectsNameModelSerializer
        else:
            return self.serializer_class

    '''
    使用action的目的是可以对原来的一些接口实现重新自定义的一些需求
    '''
    @action(methods=['get'], detail=False)  # 看url中对应的用法，需要指定什么方法，detail表示是查多个还是查一个数据
    def names(self, request):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer_obj = self.get_serializer(instance=page, many=True)
            data = serializer_obj.data
            logger.debug(data)  #收集日志
            return Response(data)
        serializer_obj = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(serializer_obj.data)

    @action(detail=True)
    def interfaces(self,request,*args,**kwargs):
        instance = self.get_object()
        serializer_obj = self.get_serializer(instance=instance)
        return Response(serializer_obj.data)





# import logging
# from django.http import HttpResponse, JsonResponse
# from django.views import View
# from django.shortcuts import render  # 用于返回html页面 重定向
# from django.db.models import Q, Count  # 组合查询
# from rest_framework.views import APIView
# from rest_framework.generics import GenericAPIView
# from rest_framework import mixins
# from interfaces.models import Interfaces
# from configures.models import Configures
# from testsuits.models import Testsuits
# from .models import Projects
# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response  # 需要结合APIview使用
# from .serializers import ProjectsModelSerializer, InterfacesByProjectsNameModelSerializer,ProjectsNamesModelSerializer,InterfacesNamesModelSerializer
# from django_filters.rest_framework import DjangoFilterBackend  # pip install django_filters
# from rest_framework.filters import OrderingFilter  # 指定排序引擎
#
# '''
# 1.ModelViewSet他继承了mixins中的增删查改与GenericViewSet，
#     class ModelViewSet(mixins.CreateModelMixin,
#                        mixins.RetrieveModelMixin,
#                        mixins.UpdateModelMixin,
#                        mixins.DestroyModelMixin,
#                        mixins.ListModelMixin,
#                        GenericViewSet):
#
# 2.根据URL中的映射关系实现了自动调用增删查改对应的接口方法
#
# 3.搞清GenericViewSet的作用（分页，过滤），搞清mixins简化增删查改的写法
#
# 搞清几个概念：
#     get—list：就是在做查询，这里查询大量数据对他们进行分页（要分页前提就需要GenericViewSet中的queryset与serializer_class），mixins.ListModelMixin下有一个list方法
#     get—retrieve：也是查询，但是是查看单条数据详情，mixins.RetrieveModelMixin下有一个retrieve方法
#     post—create：创建数据接口，mixins.CreateModelMixin下有一个create方法
#     put—update：修改接口，mixins.UpdateModelMixin下有一个update方法
#     delete—destroy，删除接口，mixins.DestroyModelMixin下有一个destroy
# '''
#
# logger = logging.getLogger('log')  #这里的log是setting中189行自己定义的名字
#
#
# '''
# 如果父类中
# '''
#
#
# class ProjectsViewSet(viewsets.ModelViewSet):
#     queryset = Projects.objects.all()  # 需要指定queryset，当前接口中需要使用到的查询集
#     serializer_class = ProjectsModelSerializer  # 需要指定serializer_class，当前接口中需要使用到的序列化器类
#     filter_backends = [DjangoFilterBackend, OrderingFilter]  # DRF框架中的过滤引擎，有它才能对下面字段进行过滤
#     filterset_fields = ['name', 'leader']  # 可根据这些字段进行过滤，任意添加模型类中的字段
#     ordering_fields = ['name', 'leader', 'id']  # 可根据这些字段进行排序，任意添加模型类中的字段
#
#
#     def list(self, request, *args, **kwargs):
#         response = super().list(request, *args, **kwargs)
#         results = response.data['results']
#         data_list = []
#         for item in results:
#             project_id = item.get("id")
#             '''
#             a.使用.annotate()方法，那么会自动使用当前模型类的主键作为分组条件
#             b.使用.annotate()方法里可以添加聚合函数，计算的名称为一般从表模型类名小写（还需要在外键字段上设置related_name）
#             c.values可以指定需要查询的字段（默认为所用字段）
#             d.可以给聚合函数指定别名，默认为testcases__count,这里的别名为testcases1
#             e.如果values发不关注annotate前面，那么聚合运算的字段不需要在values中添加
#             '''
#             interfaces_qs = Interfaces.objects.values('id').annotate(testcases=Count('testcases')).filter( project_id=project_id)
#             #获取项目下的接口总数
#             interfaces_count = interfaces_qs.count()
#
#             #获取用例总数
#             test_count = 0
#             for one_dict in interfaces_qs:
#                 test_count = test_count + one_dict.get('testcases')
#
#             #获取项目下的配置总数
#             configures_qs = Interfaces.objects.values('id').annotate(configures=Count('configures')).filter(project_id=project_id)
#             configures_count = 0
#             for one_dict in configures_qs:
#                 configures_count = configures_count + one_dict.get("configures")
#
#             #获取项目下的套件总数
#             testsuits_count = Testsuits.objects.filter(project_id=project_id).count()
#             item['interfaces'] = interfaces_count
#             item['testcases'] = test_count
#             item['testsuits'] = testsuits_count
#             item['configures'] = configures_count
#             data_list.append(item)
#             response.data['results'] = results
#         return response
#
#     # 重写父类的get_serializer_class
#     def get_serializer_class(self):
#         if self.action == 'names':
#             return ProjectsNamesModelSerializer
#         elif self.action == 'interfaces':
#             return InterfacesByProjectsNameModelSerializer
#             #return InterfacesNamesModelSerializer
#         else:
#             return self.serializer_class
#
#     '''
#     使用action的目的是可以对原来的一些接口实现重新自定义的一些需求
#     '''
#     @action(methods=['get'], detail=False)  # 看url中对应的用法，需要指定什么方法，detail表示是查多个还是查一个数据
#     def names(self, request,*args, **kwargs):
#         qs = self.get_queryset()
#         qs = self.filter_queryset(qs)
#         page = self.paginate_queryset(qs)
#         if page is not None:
#             serializer_obj = self.get_serializer(instance=page, many=True)
#             return Response(serializer_obj.data)
#         serializer_obj = self.get_serializer(instance=page,many=True)
#         return Response(serializer_obj.data)
#
#         #return self.list(request,*args, **kwargs)
#
#     @action(detail=True)
#     def interfaces(self,request,*args,**kwargs):
#         instance = self.get_object()
#         serializer_obj = self.get_serializer(instance=instance)
#         return Response(serializer_obj.data)
#
#
#
#

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

from .models import Projects
from interfaces.models import Interfaces
from configures.models import Configures
from testsuits.models import Testsuits
from .serializers import ProjectsModelSerializer, ProjectsNamesModelSerializer, \
    InterfacesByProjectIdModelSerializer, InterfacesByProjectIdModelSerializer1

# from utils.pagination import MyPagination
# 定义日志器用于记录日志，logging.getLogger('全局配置settings.py中定义的日志器名')
logger = logging.getLogger('mytest')


class ProjectsViewSet(viewsets.ModelViewSet):
    """
    list:
    获取项目的列表信息

    retrive:
    获取项目详情数据

    create:
    创建项目

    names:
    获取项目名称

    interfaces:
    获取某个项目下的接口名称
    """
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    # 如果父类中有提供相关的逻辑
    # 1、绝大部分不需要修改，只有少量要修改的，直接对父类中的action进行拓展
    # 2、绝大部分都需要修改的话，那么直接自定义即可
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        data_list = []
        for item in results:
            # item为一条项目数据所在的字典
            # 需要获取当前项目所属的接口总数、用例总数、配置总数、套件总数
            project_id = item.get('id')
            # interface_count = Interfaces.objects.filter(project_id=project_id).count()
            # interface_qs = Interfaces.objects.filter(project_id=project_id)
            # for obj in interface_qs:
            #     interface_id = obj.id
            #     TestCase.ojbects.filter(interface_id=interface_id).count()

            # a.使用.annotate()方法，那么会自动使用当前模型类的主键作为分组条件
            # b.使用.annotate()方法里可以添加聚合函数，计算的名称为一般从表模型类名小写（可以在外键字段上设置related_name）
            # c.values可以指定需要查询的字段（默认为所用字段）
            # d.可以给聚合函数指定别名，默认为testcases__count
            # e.如果values放在annotate前面，那么聚合运算的字段不需要在values中添加，放在后面需要
            # interfaces_obj = Interfaces.objects.annotate(testcases1=Count('testcases')).values('id', 'testcases1').\
            #     filter(project_id=project_id)

            interface_testcase_qs = Interfaces.objects.values('id').annotate(testcases=Count('testcases')). \
                filter(project_id=project_id)

            # 获取项目下的接口总数
            interfaces_count = interface_testcase_qs.count()

            # 定义初始用例总数为0
            testcases_count = 0
            for one_dict in interface_testcase_qs:
                testcases_count += one_dict.get('testcases')

            # 获取项目下的配置总数
            interface_configure_qs = Interfaces.objects.values('id').annotate(configures=Count('configures')). \
                filter(project_id=project_id)
            configures_count = 0
            for one_dict in interface_configure_qs:
                configures_count += one_dict.get('configures')

            # 获取项目下套件总数
            testsuites_count = Testsuits.objects.filter(project_id=project_id).count()

            item['interfaces'] = interfaces_count
            item['testcases'] = testcases_count
            item['testsuits'] = testsuites_count
            item['configures'] = configures_count
            data_list.append(item)

        response.data['results'] = data_list

        return response

    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        # return self.list(request, *args, **kwargs)
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def interfaces(self, request, *args, **kwargs):
        # instance = self.get_object()
        # # qs = Interfaces.objects.filter(projects=instance)
        # serializer_obj = self.get_serializer(instance=instance)
        # # 进行过滤和分页操作
        # return Response(serializer_obj.data)
        # return self.retrieve(request, *args, **kwargs)
        response = self.retrieve(request, *args, **kwargs)
        response.data = response.data['interfaces']
        return response

    def get_serializer_class(self):
        if self.action == 'names':
            return ProjectsNamesModelSerializer
        elif self.action == 'interfaces':
            return InterfacesByProjectIdModelSerializer
            # return InterfacesByProjectIdModelSerializer1
        else:
            return self.serializer_class

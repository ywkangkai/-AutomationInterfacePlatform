import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render #用于返回html页面 重定向
from django.db.models import Q, Count #组合查询
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .models import Projects
from rest_framework.response import Response #需要结合APIview使用
from .serializers import ProjectsModelSerializer
from django_filters.rest_framework import DjangoFilterBackend  #pip install django_filters
from rest_framework.filters import OrderingFilter #指定排序引擎


class ProjectsView(GenericAPIView):#如果要实现过滤，查询，分页等功能，需要继承GenericAPIView

    queryset = Projects.objects.all() #需要指定queryset，当前接口中需要使用到的查询集
    serializer_class = ProjectsModelSerializer #需要指定serializer_class，当前接口中需要使用到的序列化器类
    filter_backends = [DjangoFilterBackend] #DRF框架中的过滤引擎，有它才能对下面字段进行过滤
    filterset_fields = ['name','leader'] #可根据这些字段进行过滤，任意添加模型类中的字段
    ordering_fields = ['name','leader','id'] #可根据这些字段进行排序，任意添加模型类中的字段


    def get(self, request):
        qs = self.get_queryset() #这个方法就是返回上面的queryset,不直接使用self.queryset是为了提高性能，调用父类的方法是加载一次会存入缓存中，后面再用就不会在数据库中查询
        qs = self.filter_queryset(qs) #在qs的基础上课进行过滤查询
        page = self.paginate_queryset(qs) #实现分页 self.paginate_queryset()会判断PAGE_SIZE有没有值，在setting中传入了值，说明需要分页，看源码
        if page is not None:
            serializer_obj = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer_obj.data) #self.get_paginated_response此方法最终就是返回一个Response，相当于return Response(serializer_obj.data)
        serializer_obj = self.get_serializer(instance=qs, many=True)  #得到上方的序列号类
        '''
        1.Response在引入了APIView后才可用，他实现了既能放回json格式的数据，也能返回text和html的数据格式
        2.Response第一个参数是经过序列化之后的数据（往往需要使用序列化器对象.data）
        '''
        return Response(serializer_obj.data, status=200)

    def post(self, request):
        '''
        1.继承APIView后， 可以直接使用request.data的形式就能获取前段传来的json，form表单以及FILE的数据格式，格式为字典
        2.可以使用resquest.query_params来获取字符串参数
        '''

        '''
        在定义序列化器对象时，只给data传参
        使用序列化器对象.save(),会自动调用序列化器类中的create()方法
        '''
        serializer_obj = self.get_serializer(data=request.data) #使用APIview后，直接使用request.data会自动json反序列化
        serializer_obj.is_valid(raise_exception=True)
        serializer_obj.save()
        return Response(serializer_obj.data, status=201)


class ProjectDetailView(GenericAPIView):

    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer

    def get(self, request, pk):

        # try:
        #     obj = Projects.objects.get(id=pk)
        # except Exception as e:
        #     result = {
        #         "msg": "无数据",
        #         "code": 0
        #     }
        #     return Response(result, status=400)
        obj = self.get_object()  #调用父类的其实就是上述注释的逻辑
        serializer_obj = ProjectsModelSerializer(instance=obj)
        return Response(serializer_obj.data)

    def put(self, request, pk):

        '''
        如果在定义序列化器对象时，同时指定了instance和data参数，那么在调用序列化器对象的.save()方法时，会
        自动调用序列化器对象的update方法
        '''
        obj = self.get_object()
        serializer_obj = ProjectsModelSerializer(instance=obj, data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        serializer_obj.save()
        return Response(serializer_obj.data, status=201)

    def delete(self, request, pk):

        obj = self.get_object()
        obj.delete()
        return Response('success', status=200)




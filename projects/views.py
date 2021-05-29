import json
import random
import string

# 0、导入HttpResponse
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
from django.db import connection
from django.db.models import Q, Count

from .models import Projects
#from interfaces.models import Interfaces
from .serializers import ProjectsSerializer

'''
序列化器对象中几个重要的属性
1.需要调用.is_valid()方法后才能调用的属性：
    errors，validated_data 校验通过之后的数据，即数据库需要保存的数据
    
2.可以不调用.is_valid()方法直接可以访问的属性
    .data  它是最终返回给前端的数据
'''




ret = {
        "msg": "",
        "code": 0
}
class ProjectsView(View):

    def get(self, request):

        qs = Projects.objects.all()
        serializer_obj = ProjectsSerializer(instance=qs, many=True)
        return JsonResponse(serializer_obj.data, status=200, safe=False)

    def post(self, request):

        request_data = request.body
        try:
            python_data = json.loads(request_data)

        except Exception as e:
            result = {
                "msg": "参数有误",
                "code": 0
            }
            return JsonResponse(result, status=404)

        print(python_data.get("name"))
        # 1、创建序列化器对象
        # a.把前端传递的json格式参数转化为字典之后，传递给data参数
        # b.序列化器对象.is_valid()方法，开始进行校验，如果不调用此方法，那么不会进行校验
        # c.调用序列化器对象.is_valid()方法，如果校验成功，返回True，否则返回False
        # d.必须调用is_valid()方法之后，才能使用.errors属性去获取报错信息，相当于一个字典
        # e.必须调用is_valid()方法之后，才能使用.validated_data属性去获取校验通过信息，相当于一个字典

        '''
        在定义序列化器对象时，只给data传参
        使用序列化器对象.save(),会自动调用序列化器类中的create()方法
        '''
        serializer_obj = ProjectsSerializer(data=python_data)
        try:
            serializer_obj.is_valid(raise_exception=True)
        except Exception as e:
            ret['msg'] = '参数有误'
            ret.update(serializer_obj.errors)
            return JsonResponse(ret, status=404)

        serializer_obj.save()
        #serializer_obj.save(user='小明') #在调用save()方法时，传递的关键字参数，会自动添加到create方法的validated_data中
        ret['msg'] = '成功'
        ret.update(serializer_obj.validated_data)
        return JsonResponse(ret, status=201)


class ProjectDetailView(View):

    def get(self, request, pk):

        try:
            obj = Projects.objects.get(id=pk)
        except Exception as e:
            result = {
                "msg": "参数有误",
                "code": 0
            }
            return JsonResponse(result, status=400)
        print(obj.name)
        serializer_obj = ProjectsSerializer(instance=obj)
        python_dict = serializer_obj.data
        return JsonResponse(python_dict)

    def put(self, request, pk):

        try:
            obj = Projects.objects.get(id=pk)
        except Exception as e:
            result = {
                "msg": "参数有误",
                "code": 0
            }
            return JsonResponse(result, status=404)

        request_data = request.body
        try:
            python_data = json.loads(request_data)
            print(python_data)
        except Exception as e:
            result = {
                "msg": "参数有误",
                "code": 0
            }
            return JsonResponse(result, status=404)


        '''
        如果在定义序列化器对象时，同时指定了instance和data参数，那么在调用序列化器对象的.save()方法时，会
        自动调用序列化器对象的update方法
        '''
        serializer_obj = ProjectsSerializer(instance=obj, data=python_data)
        try:
            serializer_obj.is_valid(raise_exception=True)
        except Exception as e:
            ret['msg'] = '参数有误'
            ret.update(serializer_obj.errors)
            return JsonResponse(ret, status=404)

        serializer_obj.save()
        # c.向前端返回json格式的数据
        return JsonResponse(serializer_obj.data, status=201)

    def delete(self, request, pk):
        # a.校验pk值并获取待删除的模型类对象
        try:
            obj = Projects.objects.get(id=pk)
        except Exception as e:
            result = {
                "msg": "参数有误",
                "code": 0
            }
            return JsonResponse(result, status=400)

        obj.delete()

        python_data = {
            'msg': '删除成功',
            'code': 1
        }
        return JsonResponse(python_data, status=200)


# summary：
# 上述5个接口的实现步骤：
# 1.数据校验
# 2.将请求信息（json格式的字符串）转化为模型类对象（python中数据类型）
#   a.反序列化
#   b.往往为json格式的字符串（xml）
#
# 3.数据库操作（创建、更新、获取、删除）
# 4.将模型类对象转化为响应数据（json格式的字符串）返回
#  a.序列化
#  b.往往为json格式的字符串（xml）

# 有哪些痛点：
# 1.代码冗余非常大
# 2.数据校验非常麻烦
# 3.获取列表数据：没有分页操作、过滤操作、排序操作
# 4.不支持以表单来提交参数
# 5.无法自动生成接口文档

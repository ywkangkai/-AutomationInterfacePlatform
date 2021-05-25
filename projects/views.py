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

ret = {
        "msg": "",
        "code": 0
}


class ProjectsView(View):
    """
    1、需要能获取到项目的列数数据（获取多条项目数据或者所有数据）
        url: /projects/
        method：GET
        response data: json

    3、能够创建项目（创建一个项目）
        url: /projects/
        method：POST
        request data: json
        response data: json
    """
    def get(self, request):
        # a.从数据库中获取所有的项目信息(查询集)
        qs = Projects.objects.all()

        # b.需要将模型类对象（查询集）转化为嵌套字典的列表
        # python_data = []
        # python_dict = {}
        # for obj in qs:
        #     one_dict = {
        #         'id': obj.id,
        #         'name': obj.name,
        #         'leader': obj.leader
        #     }
        #     python_data.append(one_dict)
        #
        # python_dict['msg'] = '获取数据成功'
        # python_dict['code'] = 1
        # python_dict['data'] = python_data

        # 1.可以使用序列化器类来进行序列化输出
        # a.instance参数可以传模型类对象
        # b.instance参数可以传查询集（多条记录），many=True
        # c.可以ProjectsSerializer序列化器对象，调用data属性，可以将模型类对象转化为Python中的数据类型
        # d.如果未传递many=True参数，那么序列化器对象.data，返回字典，否则返回一个嵌套字典的列表
        serializer_obj = ProjectsSerializer(instance=qs, many=True)
        # c.向前端返回json格式的数据
        return JsonResponse(serializer_obj.data, status=200, safe=False)

    def post(self, request):
        # a.获取新的项目信息并转化为python中数据类型（字典或者嵌套字典的列表）
        request_data = request.body
        try:
            python_data = json.loads(request_data)
        except Exception as e:
            result = {
                "msg": "参数有误",
                "code": 0
            }
            return JsonResponse(result, status=400)

        # b.校验(非常复杂)
        # if ('name' not in python_data) or ('leader' not in python_data):
        #     result = {
        #         "msg": "参数有误",
        #         "code": 0
        #     }
        #     return JsonResponse(result, status=400)

        # 1、创建序列化器对象
        # a.把前端传递的json格式参数转化为字典之后，传递给data参数
        # b.序列化器对象.is_valid()方法，开始进行校验，如果不调用此方法，那么不会进行校验
        # c.调用序列化器对象.is_valid()方法，如果校验成功，返回True，否则返回False
        # d.必须调用is_valid()方法之后，才能使用.errors属性去获取报错信息，相当于一个字典
        # e.必须调用is_valid()方法之后，才能使用.validated_data属性去获取校验通过信息，相当于一个字典
        serializer_obj1 = ProjectsSerializer(data=python_data)
        try:
            serializer_obj1.is_valid(raise_exception=True)
        except Exception as e:
            ret['msg'] = '参数有误'
            ret.update(serializer_obj1.errors)
            return JsonResponse(ret, status=400)

        # if not serializer_obj1.is_valid():
        #     ret['msg'] = '参数有误'
        #     ret.update(serializer_obj1.errors)
        #     return JsonResponse(ret, status=400)

        # c.创建项目
        # obj = Projects.objects.create(**ret)
        obj = Projects.objects.create(**serializer_obj1.validated_data)

        # d.向前端返回json格式的数据
        # python_dict = {
        #     'id': obj.id,
        #     'name': obj.name,
        #     'leader': obj.leader,
        #     'tester': obj.tester,
        #     'programmer': obj.programmer,
        #     'code': 1,
        #     'msg': '创建成功'
        # }
        # serializer_obj = ProjectsSerializer(instance=obj)

        ret['msg'] = '成功'
        ret.update(serializer_obj1.validated_data)

        # c.向前端返回json格式的数据
        return JsonResponse(ret, status=201)


class ProjectDetailView(View):
    """
    2、需要能获取到项目的详情数据（获取前端指定某一条数据）
        url: /projects/<int:pk>/
        method：GET
        response data: json

    4、能够更新项目（只更新某一个项目）
        url: /projects/<int:pk>/
        method：PUT
        request data: json
        response data: json

    5、能够删除项目（只删除某一个项目）
        url: /projects/<int:pk>/
        method：DELETE
    """
    def get(self, request, pk):
        # a.校验参数
        try:
            obj = Projects.objects.get(id=pk)
        except Exception as e:
            result = {
                "msg": "参数有误",
                "code": 0
            }
            return JsonResponse(result, status=400)

        # b.从数据库中获取模型类对象数据
        # python_dict = {
        #     'id': obj.id,
        #     'name': obj.name,
        #     'desc': obj.programmer,
        #     'create_time': obj.create_time,
        #     'code': 1,
        #     'msg': '获取成功'
        # }
        serializer_obj = ProjectsSerializer(instance=obj)
        python_dict = serializer_obj.data

        # c.向前端返回json格式的数据
        return JsonResponse(python_dict)

    def put(self, request, pk):
        # a.校验pk值并获取待更新的模型类对象
        try:
            obj = Projects.objects.get(id=pk)
        except Exception as e:
            result = {
                "msg": "参数有误",
                "code": 0
            }
            return JsonResponse(result, status=400)

        # b.获取新的项目信息并校验
        request_data = request.body
        try:
            python_data = json.loads(request_data)
        except Exception as e:
            result = {
                "msg": "参数有误",
                "code": 0
            }
            return JsonResponse(result, status=400)

        if ('name' not in python_data) or ('leader' not in python_data):
            result = {
                "msg": "参数有误",
                "code": 0
            }
            return JsonResponse(result, status=400)

        # c.更新操作
        obj.name = python_data.get('name') or obj.name
        obj.leader = python_data.get('leader') or obj.leader
        obj.tester = python_data.get('tester') or obj.tester
        obj.programmer = python_data.get('programmer') or obj.programmer
        obj.desc = python_data.get('desc') or obj.desc
        obj.save()

        # Projects.objects.filter(id=pk).update(**python_data)
        # d.向前端返回json格式的数据
        # python_dict = {
        #     'id': obj.id,
        #     'name': obj.name,
        #     'leader': obj.leader,
        #     'tester': obj.tester,
        #     'code': 1,
        #     'msg': '更新成功'
        # }
        serializer_obj = ProjectsSerializer(instance=obj)
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

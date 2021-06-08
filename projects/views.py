import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render #用于返回html页面 重定向
from django.db.models import Q, Count #组合查询
from rest_framework.views import APIView
from .models import Projects
from rest_framework.response import Response #需要结合APIview使用
from .serializers import ProjectsModelSerializer

'''
序列化器对象中几个重要的属性
1.需要调用.is_valid()方法后才能调用的属性：
    errors，validated_data 校验通过之后的数据，即数据库需要保存的数据
    
2.可以不调用.is_valid()方法直接可以访问的属性
    .data  它是最终返回给前端的数据
'''


class ProjectsView(APIView):

    def get(self, request):

        qs = Projects.objects.all()
        serializer_obj = ProjectsModelSerializer(instance=qs, many=True)
        '''
        1.Response在引入了APIView后才可用，他实现了既能放回json格式的数据，也能返回text和html的数据格式
        2.Response第一个参数是经过序列化之后的数据（往往需要使用序列化器对象.data）
        '''
        return Response(serializer_obj.data, status=200)

    def post(self, request):
        '''
        1.继承APIView后， 可以直接使用request.data的形式就能获取前段传来的json，form表单以及FILE的数据格式，格式为字典
        2.同时支持django原生的操作，例如：
          .GET——> 查询字符串参数 ——> .query_params （get请求的用.query_params）
          .POST——> x-www-form-encode ——>
          .body——> 获取请参数体
        '''
        ret = {
            "msg": "",
            "code": 0
        }
        '''
        在定义序列化器对象时，只给data传参
        使用序列化器对象.save(),会自动调用序列化器类中的create()方法
        '''

        serializer_obj = ProjectsModelSerializer(data=request.data) #使用APIview后，直接使用request.data会自动json反序列化
        try:
            serializer_obj.is_valid(raise_exception=True)
        except Exception as e:
            ret['msg'] = '参数有误'
            ret.update(serializer_obj.errors)
            return Response(ret, status=404)

        serializer_obj.save()
        #serializer_obj.save(user='小明') #在调用save()方法时，传递的关键字参数，会自动添加到create方法的validated_data中
        ret['msg'] = '成功'
        ret.update(serializer_obj.validated_data)
        return Response(ret, status=201)


class ProjectDetailView(APIView):

    def get(self, request, pk):

        try:
            obj = Projects.objects.get(id=pk)
        except Exception as e:
            result = {
                "msg": "无数据",
                "code": 0
            }
            return Response(result, status=400)
        serializer_obj = ProjectsModelSerializer(instance=obj)
        return Response(serializer_obj.data)

    def put(self, request, pk):
        ret = {
            "msg": "",
            "code": 0
        }
        try:
            obj = Projects.objects.get(id=pk)
        except Exception as e:
            result = {
                "msg": "无数据",
                "code": 0
            }
            return Response(result, status=404)

        '''
        如果在定义序列化器对象时，同时指定了instance和data参数，那么在调用序列化器对象的.save()方法时，会
        自动调用序列化器对象的update方法
        '''
        serializer_obj = ProjectsModelSerializer(instance=obj, data=request.data)
        try:
            serializer_obj.is_valid(raise_exception=True)
        except Exception as e:
            ret['msg'] = '参数有误'
            ret.update(serializer_obj.errors)
            return Response(ret, status=404)

        serializer_obj.save()
        # c.向前端返回json格式的数据
        return Response(serializer_obj.data, status=201)

    def delete(self, request, pk):
        # a.校验pk值并获取待删除的模型类对象
        try:
            obj = Projects.objects.get(id=pk)
        except Exception as e:
            result = {
                "msg": "参数有误",
                "code": 0
            }
            return Response(result, status=204)

        obj.delete()

        python_data = {
            'msg': '删除成功',
            'code': 1
        }
        return Response(python_data, status=200)




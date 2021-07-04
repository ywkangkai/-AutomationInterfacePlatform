import os
from datetime import datetime

from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Interfaces
# from .serializers import InterfacesModelSerializer, \
#     TestcasesByInterfaceIdModelSerializer, \
#     ConfiguresByInterfaceIdModelSerializer
from . import serializers
from testcases.models import Testcases
from configures.models import Configures
from envs.models import Envs


class InterfacesViewSet(ModelViewSet):
    """
    list:
    返回接口（多个）列表数据

    create:
    创建接口

    retrieve:
    返回接口（单个）详情数据

    update:
    更新（全）接口

    partial_update:
    更新（部分）接口

    destroy:
    删除接口

    testcases:
    返回某个接口的所有用例信息（ID和名称）

    configures:
    返回某个接口的所有配置信息（ID和名称）
    """
    queryset = Interfaces.objects.all()
    serializer_class = serializers.InterfacesModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ('id', 'name')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        data_list = []
        for item in results:
            interface_id = item['id']
            # 计算用例数
            testcases_count = Testcases.objects.filter(interface_id=interface_id).count()

            # 计算配置数
            config_count = Configures.objects.filter(interface_id=interface_id).count()

            item['testcases'] = testcases_count
            item['configures'] = config_count
            data_list.append(item)
        response.data['results'] = data_list
        return response

    @action(methods=['get'], detail=True)
    def testcases(self, request, *args, **kwargs):
        """
        Returns a list of all the testcases names by interface id
        """
        # testcase_objs = Testcases.objects.filter(interface_id=pk)
        # one_list = []
        # for obj in testcase_objs:
        #     one_list.append({
        #         'id': obj.id,
        #         'name': obj.name
        #     })
        # return Response(data=one_list)

        response = self.retrieve(request, *args, **kwargs)
        response.data = response.data['testcases']
        return response

    @action(methods=['get'], detail=True)
    def configures(self, request, *args, **kwargs):
        """
        Returns a list of all the testcases names by interface id
        """
        # configures_objs = Configures.objects.filter(interface_id=pk)
        # one_list = []
        # for obj in configures_objs:
        #     one_list.append({
        #         'id': obj.id,
        #         'name': obj.name
        #     })
        # return Response(data=one_list)

        response = self.retrieve(request, *args, **kwargs)
        response.data = response.data['configures']
        return response

    def get_serializer_class(self):
        """
        不同的action选择不同的序列化器
        :return:
        """
        if self.action == "testcases":
            return serializers.TestcasesByInterfaceIdModelSerializer
        elif self.action == "configures":
            return serializers.ConfiguresByInterfaceIdModelSerializer
        else:
            return self.serializer_class

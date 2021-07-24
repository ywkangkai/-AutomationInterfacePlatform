import json
import logging
import os
from datetime import datetime

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings

from .models import Testsuits
from .serializers import TestsuitsModelSerializer, TestsuitsRunSerializer
from .utils import get_testcases_by_interface_ids
from testcases.models import Testcases
from envs.models import Envs
from utils import common


class TestsuitsViewSet(ModelViewSet):
    queryset = Testsuits.objects.all()
    serializer_class = TestsuitsModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['id', 'name']

    # def get_serializer_class(self):
    #     # if self.action == 'names':
    #     #     return EnvsNamesSerializer
    #     # else:
    #     #     return self.permission_classes
    #     return EnvsNamesSerializer if self.action == 'names' else self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {
            'name': instance.name,
            'project_id': instance.project_id,
            'include': instance.include
        }
        return Response(data)

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        # 取出并构造参数
        instance = self.get_object()
        response = super().create(request, *args, **kwargs)
        env_id = response.data.serializer.validated_data.get('env_id')
        testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        # 创建一个以时间戳命名的路径
        os.mkdir(testcase_dir_path)
        env = Envs.objects.filter(id=env_id).first()

        include = eval(instance.include)
        if len(include) == 0:
            data = {
                'ret': False,
                'msg': '此套件下未添加接口, 无法运行'
            }
            return Response(data, status=400)

        # 将include中的接口id转化为此接口下的用例id
        include = get_testcases_by_interface_ids(include)
        for testcase_id in include:
            testcase_obj = Testcases.objects.filter(id=testcase_id).first()
            if testcase_obj:
                common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        """
        不同的action选择不同的序列化器
        :return:
        """
        return TestsuitsRunSerializer if self.action == 'run' else self.serializer_class

    def perform_create(self, serializer):
        if self.action == 'run':
            pass
        else:
            serializer.save()
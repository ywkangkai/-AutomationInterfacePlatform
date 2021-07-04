import re

from rest_framework import serializers
from rest_framework import validators

from .models import Testsuits
from projects.models import Projects
from utils.common import datetime_fmt
from interfaces.models import Interfaces


def validate_include(value):
    obj = re.match(r'^\[\d+(,\d+)*\]$', value)
    if obj is None:
        raise serializers.ValidationError('参数格式有误')
    else:
        res = obj.group()
        try:
            data = eval(res)
        except:
            raise serializers.ValidationError('参数格式有误')

        for item in data:
            if not Interfaces.objects.filter(id=item).exists():
                raise serializers.ValidationError(f'接口id【{item}】不存在')


class TestsuitsModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.all(), write_only=True)

    class Meta:
        model = Testsuits
        fields = ('id', 'name', 'project', 'project_id', 'include', 'create_time', 'update_time')

        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': datetime_fmt()
            },
            'update_time': {
                'read_only': True,
                'format': datetime_fmt()
            },
            'include': {
                # 'write_only': True,
                'validators': [validate_include]
            }
        }

    def create(self, validated_data):
        project = validated_data.pop('project_id')
        validated_data['project'] = project
        # testsuit = Testsuits.objects.create(**validated_data)
        # return testsuit
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
            return super().update(instance, validated_data)

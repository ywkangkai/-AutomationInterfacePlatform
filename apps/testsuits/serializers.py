from rest_framework import serializers
from testsuits.models import Testsuits
from projects.models import Projects
from utils.format_time import datetimes_fmt
from interfaces.models import Interfaces
import re


'''
校验include关联接口传参格式，格式为[1,2,3]，非此格式传入报错
'''
def validata_include(value):
    obj = re.match(r'^\[\d+(,\d+)*\]$')
    if obj is None:
        raise serializers.ValidationError('参数格式有误 ')
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

    project = serializers.StringRelatedField(label='所属项目id', help_text='所属项目id')
    project_id = serializers.PrimaryKeyRelatedField(write_only=True, label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.all())

    class Meta:
        model = Testsuits
        fields = ('id','name','project','project_id','include','create_time','update_time')
        extra_kwargs = {
            'create_time':{
                'read_only': True,
                'format':datetimes_fmt()
            },
            'update_time': {
                'read_only':True,
                'format': datetimes_fmt()
            },
            'include': {
                'write_only': True,
                'validators': [validata_include]
            },
        }

    def create(self, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop("project_id")
            validated_data['project'] = project.id
            return super().create(validated_data)

    '''
    将project_id去掉是因为上方的project_id得到的是一个模型对象
    而传入的时候只需要传入id，所以先把此对象去掉，增加一个id值
    '''
    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop("project_id")
            validated_data['project'] = project.id
            return super().update(instance, validated_data)
from rest_framework import serializers

from interfaces.models import Interfaces
from utils import validates
from .models import Configures


class InterfacesAnotherSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(help_text='项目名称')
    pid = serializers.IntegerField(label='所属项目id', help_text='所属项目id', write_only=True,
                                   validators=[validates.is_exised_project_id])
    iid = serializers.IntegerField(label='所属接口id', help_text='所属接口id', write_only=True,
                                   validators=[validates.is_exised_interface_id])

    class Meta:
        model = Interfaces
        fields = ('iid', 'name', 'project', 'pid')
        extra_kwargs = {
            'name': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        """
        校验项目ID是否与接口ID一致
        :param attrs:
        :return:
        """
        if not Interfaces.objects.filter(id=attrs['iid'], project_id=attrs['pid']).exists():
            raise serializers.ValidationError("项目和接口信息不对应!")
        return attrs


class ConfiguresSerializer(serializers.ModelSerializer):
    """
    配置序列化器
    """
    interface = InterfacesAnotherSerializer(help_text='项目ID和接口ID')

    class Meta:
        model = Configures
        fields = ('id', 'name', 'interface', 'author', 'request')
        extra_kwargs = {
            'request': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        interface_dict = validated_data.pop('interface')
        validated_data['interface_id'] = interface_dict['iid']
        return Configures.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'interface' in validated_data:
            interface_dict = validated_data.pop('interface')
            validated_data['interface_id'] = interface_dict['iid']
        return super().update(instance, validated_data)

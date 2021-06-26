from rest_framework import serializers
from interfaces.models import Interfaces
from projects.models import Projects
from utils.format_time import datetimes_fmt



class InterfacesModelSerializer(serializers.ModelSerializer):

    project = serializers.StringRelatedField(label='所属项目id', help_text='所属项目id',read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(write_only=True, label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.all())

    class Meta:
        model = Interfaces
        fields = ('id','name','project','project_id','tester','create_time',)

        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': datetimes_fmt(),
            }
        }


    # def create(self, validated_data):
    #     print(validated_data)
    #     interface = super().create(validated_data)
    #     return interface
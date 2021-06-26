from rest_framework import serializers
from envs.models import Envs
from utils.format_time import datetimes_fmt


class EnvsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Envs
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': datetimes_fmt(),
            }
        }



class EnvsNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Envs
        fields = ('id','name')

from rest_framework import serializers
from rest_framework import validators

from .models import Envs
from utils import common


class EnvsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Envs
        exclude = ('update_time', )

        extra_kwargs = {
            'create_time': {
                # 'read_only': False,
                'read_only': True,
                'format': common.datetime_fmt(),
            },

        }


class EnvsNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envs
        fields = ('id', 'name')

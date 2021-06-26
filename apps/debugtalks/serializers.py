from rest_framework import serializers
from interfaces.models import Interfaces
from rest_framework import validators
from debugtalks.models import DebugTalks


class DebugTalksModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DebugTalks
        fields = ('debugtalk','project')


from rest_framework import serializers
from interfaces.models import Interfaces
from rest_framework import validators

class InterfacesModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = Interfaces
        fields = '__all__'  #fileds类属性来指定模型类中哪些字段需要输入或输出


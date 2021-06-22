from rest_framework import serializers
from interfaces.models import Interfaces
from rest_framework import validators
from projects.models import Projects
class InterfacesModelSerializer(serializers.ModelSerializer):
    '''
    子表查父表不用  字段_set，project与project_id两种写法都行，这里主要是为一个查父表的name一个查父表的ID
    '''
    prject = serializers.StringRelatedField() #StringRelatedField会返回project表__str__返回的字段   name
    project_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Projects.objects.all()) # project_id其实与prject是一样的性质，都是为了查父表，这里主要是id

    class Meta:
        model = Interfaces
        fields = '__all__'  #fileds类属性来指定模型类中哪些字段需要输入或输出


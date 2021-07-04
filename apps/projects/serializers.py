# from rest_framework import serializers
# from projects.models import Projects
# from rest_framework import validators
# from interfaces.models import Interfaces
# from interfaces.serializers import InterfacesModelSerializer
# from utils.format_time import datetimes_fmt
# from debugtalks.models import DebugTalks
# '''
# 自定义调用字段校验，value是前端传入的字段，如在name字段调用此函数，value=name，如果校验失败一定使用
# raise serializers.ValidationError
# '''
# def is_name_contain_x(value):
#     if 'x' in value:
#         raise serializers.ValidationError('项目名称不能包含x')
#
# def is_name_contain_y(value):
#     if 'y' in value:
#         raise serializers.ValidationError('项目名称不能包含y')
#
#
# class ProjectsSerializer(serializers.Serializer):
#     """
#     可以定义序列化器类，来实现序列化和反序列化操作
#     a.一定要继承serializers.Serializer或者Serializer的子类
#     b.默认情况下，可以定义序列化器字段，序列化器字段名要与模型类中字段名相同
#     c.默认情况下，定义几个序列化器字段，那么就会返回几个数据（到前端，序列化输出的过程），前端也必须得传递这几个字段（反序列化过程）
#     """
#     # default_error_messages = {
#     #     'required': "改字段必传",
#     #     'null': "改字段不能为空"
#     # }
#     # d.CharField、BooleanField、IntegerField与模型类中的字段类型一一对应
#     # e.required参数默认为None，指定前端必须得传此字段，如果设置为False的话，前端可以不传此字段
#     # f.label和help_text -> verbose_name和help_text一一对应
#     # g.allow_null指定前端传递参数时可以传空值
#     # CharField字段，max_length指定该字段不能操作的字节参数，
#
#     '''
#     1、使用validators函数，可以指定校验规则
#     校验规则：
#         a、djangorestframework自带校验规则(UniqueValidator,第一个参数需要设置查询集，第二个参数message指定校验失败后的信息)
#         b、自定义校验规则，见上方
#     '''
#     name = serializers.CharField(max_length=10, label='项目名称', help_text='项目名称', min_length=2,
#                                  validators=[validators.UniqueValidator(Projects.objects.all(), message='项目已存在',
#                                                                         ), is_name_contain_x, is_name_contain_y])
#     # leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人')
#     # h.如果某个字段指定read_only=True，那么此字段，前端在创建数据时（反序列化过程）可以不用传，但是一定会输出（序列化过程）
#     # i.字段不能同时指定read_only=True, required=True
#     # leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人', read_only=True, required=True)
#     leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人', read_only=True)
#     # tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员')
#     # j.如果某个字段指定write_only=True，那么此字段只能进行反序列化输入，而不会输出（创建数据时必须得传，但是不返回）
#     # k.可以给字段添加error_messages参数，为字典类型，字典的key为校验的参数名，值为校验失败之后错误提示
#     tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员', write_only=True,
#                                    error_messages={"required": "该字段必传", "max_length": "长度不能操作200个字节"})
#     # k.一个字段不同同时指定write_only=True, read_only=True
#     # tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员', write_only=True, read_only=True)
#
#     '''
#     此方法的字段校验与上方的自定义校验的区别是:
#         1、validate_name,其中name是字段名称，形式为validate_xxxx，
#         2、此写法不需要将函数进行调用会自行进行校验,需要注意的是必须要将value进行返回
#         3、当上方字典中的规则都未通过时，不会进入这里的校验
#     '''
#     def validate_name(self, value):
#         if '非常' in value:
#             raise serializers.ValidationError('项目名称中不能包含非常')
#         return value
#
#     def validate_tester(self, value):
#         if len(value) != 8:
#             raise serializers.ValidationError('测试人员姓名必须输入8位')
#         return value
#
#     '''
#     多字段校验，attr['xxx']可以获取某个字段的值
#     必须要返回attrs
#     '''
#     def validate(self, attrs):
#         if attrs['name'] != attrs['leader']:
#             raise serializers.ValidationError("两个字段不一致")
#         return attrs
#     #############################################################
#
#     def create(self, validated_data):
#         #validated_data为校验通过之后的数据,必须返回对象
#         obj = Projects.objects.create(**validated_data)
#         return obj
#
#
#     def update(self, instance, validated_data):
#         # c.更新操作
#         print(validated_data)
#         instance.name = validated_data.get('name') or instance.name
#         instance.leader = validated_data.get('leader') or instance.leader
#         instance.tester = validated_data.get('tester') or instance.tester
#         instance.programmer = validated_data.get('programmer') or instance.programmer
#         instance.desc = validated_data.get('desc') or instance.desc
#         instance.save()
#
#         return instance
#
#
#
# '''
# 使用模型序列化器类，简化序列化器类中字段的创建
# 需要继承ModelSerializer，但是不需要在重写create和update方法，调用.save()方法后可以直接调用create与update方法
# '''
# class ProjectsModelSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(max_length=10, label='项目名称', help_text='项目名称', min_length=2,
#                                  validators=[validators.UniqueValidator(Projects.objects.all(), message='项目已存在',
#                                                                         ), is_name_contain_x, is_name_contain_y])
#     #email = serializers.EmailField() #可以添加模型类中没有的字段，但必须要写入到fields中，场景：验证码，需要校验，但无需校验字段
#     #此处的interfaces是在接口表interfaces中的project字段中有一个related_name=interfaces属性，如果这个属性等于其他值就需要跟着变化，如果没有related_name这个属性需要写为interfaces_set
#     interfaces = InterfacesModelSerializer(many=True,read_only=True)
#     #interfaces = serializers.StringRelatedField() 这个属性是返回接口表interfaces中   def __str__(self):
#     class Meta:
#         #需要在Meta内部类这两个指定model类属性，需要按照哪一个模型来创建
#         #默认id主键，会添加read_only=True
#         #create_time和update_time，会添加read_only=True
#         model = Projects
#         #fields = '__all__'  #fileds类属性来指定模型类中哪些字段需要输入或输出
#         #fields = ('id','name','leader','tester','interfaces')#可以将需要输入或输出的字段，在元组中指定
#         exclude = ('update_time',)#把不需要输入和输出的字段排除
#         #read_only_fields = ('id','desc') #这些字段只输出不输入
#         extra_kwargs = {
#               'create_time':{
#                   'read_only':True,
#                   'format': datetimes_fmt(),
#               }
#         }
#
#     def create(self, validated_data):
#         #业务：在创建项目时需要创建一个空的debugtalk.py文件
#         project = super().create(validated_data)
#         DebugTalks.objects.create(project=project)
#         return project
#
#     #添加了email字段，但是该字段不在表中，所以在创建数据时需要先将该字段剔除
#     # def create(self, validated_data):
#     #     email = validated_data.pop("email")
#     #     return Projects.objects.create(**validated_data)
#
# class ProjectsNamesModelSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Projects
#         fields = ('id','name')
#
#
# class InterfacesNamesModelSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Interfaces
#         fields = ('id','name')
#
#
# class InterfacesByProjectsNameModelSerializer(serializers.ModelSerializer):
#
#     interfaces = InterfacesNamesModelSerializer(many=True, read_only=True)
#     class Meta:
#         model = Projects
#         fields = ('interfaces',)


# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/7/1 20:14
  @Auth : 可优
  @File : serializers.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
from rest_framework import serializers
from rest_framework import validators

from .models import Projects
from interfaces.models import Interfaces
from interfaces.serializers import InterfacesModelSerializer
from utils.format_time import datetimes_fmt
from debugtalks.models import DebugTalks


class InterfacesNamesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interfaces
        fields = ('id', 'name')


class ProjectsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        exclude = ('update_time', )

        extra_kwargs = {
            'create_time': {
                'read_only': False,
                'format': datetimes_fmt(),
            },

        }

    def create(self, validated_data):
        # 在创建项目时，同时创建一个空的debugtalk.py文件
        project = super().create(validated_data)
        DebugTalks.objects.create(project=project)
        return project


class ProjectsNamesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ('id', 'name')


class InterfacesByProjectIdModelSerializer(serializers.ModelSerializer):
    interfaces = InterfacesNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Projects
        fields = ('interfaces', )


class InterfacesByProjectIdModelSerializer1(serializers.ModelSerializer):
    # interfaces = InterfacesNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Interfaces
        fields = ('id', 'name')

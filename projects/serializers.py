from rest_framework import serializers

class ProjectsSerializer(serializers.Serializer):
    """
    可以定义序列化器类，来实现序列化和反序列化操作
    a.一定要继承serializers.Serializer或者Serializer的子类
    b.默认情况下，可以定义序列化器字段，序列化器字段名要与模型类中字段名相同
    c.默认情况下，定义几个序列化器字段，那么就会返回几个数据（到前端，序列化输出的过程），前端也必须得传递这几个字段（反序列化过程）
    """
    # default_error_messages = {
    #     'required': "改字段必传",
    #     'null': "改字段不能为空"
    # }

    # d.CharField、BooleanField、IntegerField与模型类中的字段类型一一对应
    # e.required参数默认为None，指定前端必须得传此字段，如果设置为False的话，前端可以不传此字段
    # f.label和help_text -> verbose_name和help_text一一对应
    # g.allow_null指定前端传递参数时可以传空值
    # CharField字段，max_length指定该字段不能操作的字节参数，
    name = serializers.CharField(max_length=10, label='项目名称', help_text='项目名称', min_length=2)
    # leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人')
    # h.如果某个字段指定read_only=True，那么此字段，前端在创建数据时（反序列化过程）可以不用传，但是一定会输出（序列化过程）
    # i.字段不能同时指定read_only=True, required=True
    # leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人', read_only=True, required=True)
    leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人', read_only=True)
    # tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员')
    # j.如果某个字段指定write_only=True，那么此字段只能进行反序列化输入，而不会输出（创建数据时必须得传，但是不返回）
    # k.可以给字段添加error_messages参数，为字典类型，字典的key为校验的参数名，值为校验失败之后错误提示
    tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员', write_only=True,
                                   error_messages={"required": "该字段必传1", "max_length": "长度不能操作200个字节"})
    # k.一个字段不同同时指定write_only=True, read_only=True
    # tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员', write_only=True, read_only=True)

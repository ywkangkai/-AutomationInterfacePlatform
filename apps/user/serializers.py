from rest_framework import serializers
from rest_framework import validators
from django.contrib.auth.models import User  # 这个user表示django内置提供
from rest_framework_jwt.serializers import jwt_payload_handler,jwt_encode_handler

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        label='用户名',
        max_length=20,
        min_length=6,
        validators=[
            validators.UniqueValidator(
                User.objects.all(),
                message='用户已存在')],
        error_messages={
            'min_length': '仅允许输入6-20个字符',
            'max_length': '仅允许输入6-20个字符'})

    password_confirm = serializers.CharField(
        max_length=20,
        min_length=6,
        write_only=True,
        label="确认密码",
        error_messages={
            'min_length': '仅允许输入6-20个字符',
            'max_length': '仅允许输入6-20个字符'})

    token = serializers.CharField(label='生成token', read_only=True)

    email = serializers.EmailField(
        label='邮箱',
        write_only=True,
        required=True,
        validators=[
            validators.UniqueValidator(
                User.objects.all(),
                message='邮箱已存在')])

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'email', 'token')

    def create(self, validated_data):
        # validated_data为校验通过之后的数据,必须返回对象
        validated_data.pop("password_confirm")
        #obj = User.objects.create(**validated_data)
        #创建了一个用户模型，理解为实例化了一个用户
        user = User.objects.create_user(**validated_data)  #create_user这个是django内置的，会自动帮密码进行加密处理（该方法只针对创建用户使用）

        #创建token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token   #当创建一个用户后django源码会自动给你用户模型添加一个token=None的属性，此时我们只需要把自己生成的token赋值给它
        return user

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("密码输入不一致")
        return attrs

from rest_framework import serializers

class ProjectsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, label='项目名称', help_text='项目名称')
    leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人')
    tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员')
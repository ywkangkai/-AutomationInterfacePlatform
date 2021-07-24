import logging, json, os
from reports.models import Reports
from rest_framework import viewsets
from .serializers import ReportsModelSerializer
from rest_framework.response import Response
from django.http.response import StreamingHttpResponse
from rest_framework.decorators import action
from django.conf import settings
from django.utils.encoding import escape_uri_path
from utils.download_file import get_file_content




class ReportsViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsModelSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        try:
            # 将summary json字符串转化为Python中的字典类型
            response.data['summary'] = json.loads(response.data['summary'], encoding='utf-8')
        except Exception as e:
            pass
        return response

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        # 获取html源码
        instance = self.get_object()
        html = instance.html
        name = instance.name

        # 获取测试报告所属目录路径
        report_dir = settings.REPORT_DIR

        # 生成html文件，存放到reports目录下
        report_full_dir = os.path.join(report_dir, name) + '.html'
        if not os.path.exists(report_full_dir):
            with open(report_full_dir, 'w', encoding='utf-8') as file:
                file.write(html)

        # 获取文件流，返回给前端
        # 创建一个生成器，获取文件流，每次获取的是文件字节数据

        response = StreamingHttpResponse(get_file_content(report_full_dir))

        html_file_name = escape_uri_path(name + '.html')
        # 添加响应头
        # 直接使用Response对象['响应头名称'] = '值'
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f"attachement; filename*=UTF-8''{html_file_name}"

        # return StreamingHttpResponse(get_file_content(report_full_dir))
        return response


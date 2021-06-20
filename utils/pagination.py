from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class MyPagination(PageNumberPagination):

    page_size = 10  #修改每页显示的条数

    page_query_param = 'page'  #查看第N页的数据 http://IP?p=n

    page_size_query_param = 'size' #http://IP?s=n   相当于可以修改page_size，控制页面显示的个数，优先级高于page_size

    max_page_size = 50  #控制每页最大的显示个数，当page_size大于max_page_size，他的优先级高于page_size与page_size_query_param

    page_query_description = '第几页'

    page_size_query_description = '每页几条'


    def get_paginated_response(self, data):
        current_page_num = self.page.number  #获取当前在第几页
        total_pages = self.page.paginator.num_pages #获取总页数
        response = super().get_paginated_response(data)
        response.data["curent_page_num"] = current_page_num
        response.data["total_pages"] = total_pages
        return response
        # return Response(OrderedDict([
        #     ('count',self.page.paginator.count),
        #     ('next', self.get_next_link()),
        #     ('previous', self.get_previous_link()),
        #     ('results', data),
        #     ('curent_page_num', current_page_num),
        #     ('total_pages', total_pages)
        # ]))
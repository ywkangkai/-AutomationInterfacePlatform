from rest_framework.pagination import PageNumberPagination

class MyPagination(PageNumberPagination):

    page_size = 3  #修改每页显示的条数

    page_query_param = 'p'  #查看第N页的数据 http://IP?p=n

    page_size_query_param = 's' #http://IP?s=n   相当于可以修改page_size，控制页面显示的个数，优先级高于page_size

    max_page_size = 2  #控制每页最大的显示个数，当page_size大于max_page_size，他的优先级高于page_size与page_size_query_param
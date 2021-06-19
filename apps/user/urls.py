from django.urls import path, re_path

# from projects.views import
from projects import views
from rest_framework.routers import DefaultRouter,SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

'''
需要集成ViewSet才能使用这种写法，
使用映射关系，根据不通的路径去找不通的方法
'''
urlpatterns = [
    path('login/', obtain_jwt_token),

]

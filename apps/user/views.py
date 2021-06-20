from django.shortcuts import render
from user.serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView

class UserView(CreateAPIView):

    # def post(self,request):   这是继承APIView的写法
    #     serializer_job = RegisterSerializer(data=request.data)
    #     serializer_job.is_valid(raise_exception=True)
    #     serializer_job.save()
    #     return Response(serializer_job.data)

    serializer_class = RegisterSerializer   #CreateAPIView会自动调用create方法，相当于上面的逻辑



#此接口是在注册的时候，当输入了用户名前端会发起请求先判断一次是否有注册过
class UsernameIsExistedView(APIView):

    def get(self,request, username):
        user_query = User.objects.filter(username=username)
        count = user_query.count()
        count_dict = {
            'count':count,
            'username':username
        }
        return Response(count_dict)


#同上
class EmailIsExistedView(APIView):

    def get(self,request, email):
        email_query = User.objects.filter(email=email)
        count = email_query.count()
        count_dict = {
            'count':count,
            'email':email
        }
        return Response(count_dict)


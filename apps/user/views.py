from django.shortcuts import render
from user.serializers import UserModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

class UserView(APIView):

    def post(self,request):
        serializer_job = UserModelSerializer(data=request.data)
        serializer_job.is_valid(raise_exception=True)
        serializer_job.save()
        return Response(serializer_job.data)



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


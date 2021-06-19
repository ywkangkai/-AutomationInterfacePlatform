from django.shortcuts import render
from user.serializers import UserModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class UserView(APIView):

    def post(self,request):
        serializer_job = UserModelSerializer(data=request.data)
        serializer_job.is_valid(raise_exception=True)
        serializer_job.save()
        return Response(serializer_job.data)






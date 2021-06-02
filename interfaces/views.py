import json
import random
import string
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
from django.db import connection
from django.db.models import Q, Count
from .models import Interfaces
from .serializers import InterfacesModelSerializer



class InterfacesView(View):

    def get(self, request):
        qs = Interfaces.objects.all()
        serializer_obj = InterfacesModelSerializer(instance=qs, many=True)
        return JsonResponse(serializer_obj.data, status=200, safe=False) #加safe=False的原因是，接口表与项目表关联，查询出来的数据存在列表的形式
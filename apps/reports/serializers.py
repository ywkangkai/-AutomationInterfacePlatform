from rest_framework import serializers
from utils.format_time import datetimes_fmt
from reports.models import Reports
import re




class ReportsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reports
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time':{
                'format':datetimes_fmt()
            },
            'update_time': {
                'format': datetimes_fmt()
            },
            'html': {
                'write_only': True,
            },
        }


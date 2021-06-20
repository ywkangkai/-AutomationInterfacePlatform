from django.db import models

#写这个基类的目的是，所有表都有这个两个字段，所以抽出来单独继承
class BaseModel(models.Model):

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        #指定在迁移时不创建表
        abstract = True
from django.db import models
from utils.base_models import BaseModel
# Create your models here.
# 一个mysql软件中，可以有多个数据库
# 一个数据库中，可以有多张数据表
# 一张数据表中，有多条数据（多条记录）以及多个字段（多个列）


# 1、可以在子应用projects/models.py文件中，来定义数据模型
# 2、一个数据模型类对应一个数据表
# 3、数据模型类，需要继承Model父类或者Model子类
# 4、在数据模型类中，添加的类属性（Field对象）来对应数据表中的字段
# 5、创建完数据库模型类之后，需要迁移才能生成数据表
# a.生成迁移脚本，放在projects/migrations目录中：python manage.py makemigrations
# b.执行迁移脚本：python manage.py migrate
# c.如果不添加选项，那么会将所有子应用进行迁移
# 6、会自动创建字段名为id的类属性，自增、主键、非空
class Projects(BaseModel):
    # 7、只要某一个字段中primary_key=True，那么Django就不会自动创建id字段，会使用自定义的
    # 8、CharField -> varchar
    # IntegerField -> int
    # TextField -> text
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    # 9、verbose_name为个性化信息
    # 10、help_text帮助文本信息，在api接口文档平台和admin后端站点中会用于提示，往往跟verbose_name一致
    # 11、unique用于指定唯一键，默认为False
    # 12、CharField至少要指定一个max_length必传参数，代表此字段的最大长度，不能为负数
    name = models.CharField('项目名称', max_length=200, unique=True, help_text='项目名称')
    leader = models.CharField('负责人', max_length=50, help_text='项目负责人')
    tester = models.CharField('测试人员', max_length=50, help_text='项目测试人员')
    programmer = models.CharField('开发人员', max_length=50, help_text='开发人员')
    publish_app = models.CharField('发布应用', max_length=100, help_text='发布应用')
    # 13、null指定数据在保存时是否可以为空，默认不能为空，如果null=True，那么可以为空值
    # 14、blank指定前端用户在创建数据时，是否需要传递，默认需要传递，如果不传递，需要blank设置为True
    # 15、default为某一个字段指定默认值，往往会跟blank一起使用
    desc = models.CharField('简要描述', max_length=200, null=True, blank=True, default='', help_text='简要描述')

    # 16、DateTimeField可以添加auto_now_add选项，django会自动添加创建记录时的时间
    #create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    # 17、DateTimeField可以添加auto_now选项，django会自动添加更新记录时的时间
    #update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    # 18、执行迁移脚本之后，生成的数据表名默认为 子应用名_模型类名小写

    class Meta:
        # 19、可以在模型类下定义Meta子类，Meta子类名称固定
        # 20、可以使用db_table类属性，来指定表名
        db_table = 'tb_projects'
        # 21、指定表的个性化描述
        verbose_name = '项目信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"<{self.name}>"


# Generated by Django 2.2.7 on 2021-06-02 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interfaces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='接口名称', max_length=200, unique=True, verbose_name='接口名称')),
                ('tester', models.CharField(help_text='测试人员', max_length=50, verbose_name='测试人员')),
                ('desc', models.CharField(blank=True, help_text='简要描述', max_length=200, null=True, verbose_name='简要描述')),
                ('projects', models.ForeignKey(help_text='所属项目', on_delete=django.db.models.deletion.CASCADE, related_name='interfaces', to='projects.Projects', verbose_name='所属项目')),
            ],
            options={
                'verbose_name': '接口信息',
                'verbose_name_plural': '接口信息',
                'db_table': 'tb_interfaces',
            },
        ),
    ]

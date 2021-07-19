
import json
import locale
import os
from datetime import datetime

from rest_framework.response import Response
import yaml
from httprunner.task import HttpRunner
from httprunner.report import render_html_report

from debugtalks.models import DebugTalks
from configures.models import Configures
from testcases.models import Testcases
from reports.models import Reports


def datetime_fmt():
    locale.setlocale(locale.LC_CTYPE, 'chinese')
    return '%Y年%m月%d日 %H:%M:%S'


def create_report(runner, report_name=None):
    """
    创建测试报告
    :param runner:
    :param report_name:
    :return:
    """
    time_stamp = int(runner.summary["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner.summary['time']['start_datetime'] = start_datetime

    # duration保留3位小数
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    runner.summary['html_report_name'] = report_name

    for item in runner.summary['details']:
        # 对时间戳进行处理
        try:
            time_stamp = int(item['time']['start_at'])
            detail['time']['start_at'] = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass

        try:
            for record in item['records']:
                # 对时间戳进行处理
                try:
                    time_stamp = int(record['meta_data']['request']['start_timestamp'])
                    record['meta_data']['request']['start_timestamp'] = \
                        datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
                except Exception:
                    pass

                record['meta_data']['response']['content'] = record['meta_data']['response']['content']. \
                    decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request']['body']
                if isinstance(request_body, bytes):
                    record['meta_data']['request']['body'] = request_body.decode('utf-8')
        except Exception as e:
            continue

    summary = json.dumps(runner.summary, ensure_ascii=False)

    report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    report_path = runner.gen_html_report(html_report_name=report_name)

    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()

    test_report = {
        'name': report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('successes'),
        'count': runner.summary.get('stat').get('testsRun'),
        'html': reports,
        'summary': summary
    }
    report_obj = Reports.objects.create(**test_report)
    return report_obj.id


def generate_testcase_file(instance, env, testcase_dir_path):
    testcase_list = []
    config = {
        'config': {
            'name': instance.name,
            'request': {
                'base_url': env.base_url if env else ''
            }
        }
    }
    testcase_list.append(config)

    # 获取include信息
    include = json.loads(instance.include, encoding='utf-8')
    # 获取request字段
    request = json.loads(instance.request, encoding='utf-8')
    # 获取用例所属接口名称
    interface_name = instance.interface.name
    # 获取用例所属项目名称
    project_name = instance.interface.project.name

    testcase_dir_path = os.path.join(testcase_dir_path, project_name)

    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
        # 生成debugtalk.py文件，放到项目根目录下
        debugtalk_obj = DebugTalks.objects.filter(project__name=project_name).first()
        debugtalk = debugtalk_obj.debugtalk if debugtalk_obj else ''
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'), 'w', encoding='utf-8') as f:
            f.write(debugtalk)

    testcase_dir_path = os.path.join(testcase_dir_path, interface_name)
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    # {"config":1,"testcases":[1,2,3]}
    if 'config' in include:
        config_id = include.get('config')
        config_obj = Configures.objects.filter(id=config_id).first()
        if config_obj:
            config_request = json.loads(config_obj.request, encoding='utf-8')
            config_request['config']['request']['base_url'] = env.base_url if env else ''
            testcase_list[0] = config_request

    # 处理前置用例
    if 'testcases' in include:
        for testcase_id in include.get('testcases'):
            testcase_obj = Testcases.objects.filter(id=testcase_id).first()
            try:
                testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
            except Exception as e:
                continue

            testcase_list.append(testcase_request)

    # 把当前需要执行的用例追加到testcase_list最后
    testcase_list.append(request)
    # with open(os.path.join(testcase_dir_path, instance.name + '.yaml'), 'w', encoding='utf-8') as f:
    #     yaml.dump(testcase_list, f, all_unicode=True)

    with open(os.path.join(testcase_dir_path, instance.name + '.yaml'), 'w', encoding='utf-8') as f:
        print(testcase_list)
        yaml.dump(testcase_list, f, allow_unicode=True)


def run_testcase(instance, testcase_dir_path):
    # 1、运行用例
    runner = HttpRunner()
    try:
        runner.run(testcase_dir_path)
    except Exception as e:
        res = {'ret': False, 'msg': '用例执行失败'}
        return Response(res, status=400)

    # 2、创建报告
    report_id = create_report(runner, instance.name)

    # 3、用例运行成功之后，需要把生成的报告id返回
    data = {
        'id': report_id
    }
    return Response(data, status=201)

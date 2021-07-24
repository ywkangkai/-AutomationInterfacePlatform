# debugtalk.py
import random
import time


def sleep(n_secs):
    time.sleep(n_secs)


def get_user_agent():
    user_agents = ["Mozilla/5.0 BenBen", "Mozilla/5.0 MaZai", "Mozilla/5.0 icon"]
    return random.choice(user_agents)


def get_accounts():
    accounts = [
        {"title": "正常登录", "username": "keyou1", "password": "123456",
            "status_code": 200, "contain_msg": "token"},
        {"title": "密码错误", "username": "keyou1", "password": "123457",
            "status_code": 400, "contain_msg": "non_field_errors"},
        {"title": "账号错误", "username": "keyou1111", "password": "123456",
            "status_code": 400, "contain_msg": "non_field_errors"},
        {"title": "用户名为空", "username": "", "password": "123456",
            "status_code": 400, "contain_msg": "username"},
        {"title": "密码为空", "username": "keyou1", "password": "",
            "status_code": 400, "contain_msg": "password"},
    ]
    return accounts


def get_project_name():
    old_project_name = []
    while True:
        project_name = "这是一个跨时代的{}项目".format(random.randint(0, 10000))
        if project_name not in old_project_name:
            old_project_name.append(project_name)
            return project_name


def create_project():
    projects = [
        {
            "title": "正常创建项目",
            "name": get_project_name(),
            "leader": "可优",
            "tester": "可可",
            "programmer": "优优",
            "publish_app": "国产大飞机C919研制应用",
            "desc": "此项目会提升民族自信心",
            "status_code": 201
        },
        {
            "title": "项目名为空",
            "name": None,
            "leader": "小可可",
            "tester": "可可",
            "programmer": "优优",
            "publish_app": "国产大飞机C919研制应用",
            "desc": "此项目会提升民族自信心",
            "status_code": 400
        },
        {
            "title": "leader为空",
            "name": get_project_name(),
            "leader": None,
            "tester": "可可",
            "programmer": "优优",
            "publish_app": "国产大飞机C919研制应用",
            "desc": "此项目会提升民族自信心",
            "status_code": 400
        },
        {
            "title": "tester为空",
            "name": get_project_name(),
            "leader": "小优优",
            "tester": None,
            "programmer": "优优",
            "publish_app": "国产大飞机C919研制应用",
            "desc": "此项目会提升民族自信心",
            "status_code": 400
        },
    ]

    return projects
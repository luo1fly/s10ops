#!/usr/bin/env python
# Name: multi_task.py
# Time:8/14/16 10:15 PM
# Author:luo1fly

import sys
import re
import os
# import json
from getopt import getopt, GetoptError
# print(os.path.abspath(__file__))
sys.path.append(
    os.path.dirname(    # /root/PycharmProjects/s10ops
        os.path.dirname(    # /root/PycharmProjects/s10ops/hosts
            os.path.dirname(    # /root/PycharmProjects/s10ops/hosts/backend
                os.path.abspath(__file__)   # /root/PycharmProjects/s10ops/hosts/backend/multi_task.py
            )
        )
    )
)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 's10ops.settings')
import django
django.setup()
# 以上是从外部引用django的settings需要做的事情
from hosts import models
from django.core.exceptions import ObjectDoesNotExist
from multiprocessing import Pool
from paramiko_handler import paramiko_ssh, paramiko_sftp
# import custom modules above


def by_paramiko(task_id):
    try:
        task_obj = models.TaskLog.objects.get(id=task_id)
        # print('task_obj:', task_obj.cmd)
    except ObjectDoesNotExist as e:
        sys.exit(e.args[0])
    else:
        def multi_call(func):
            pool = Pool(processes=2)
            for bind_host_to_user_obj in task_obj.hosts.select_related():
                pool.apply_async(func, args=(bind_host_to_user_obj, task_obj, task_id))
            pool.close()
            pool.join()

        if task_obj.task_type == 'multi_cmd':
            multi_call(paramiko_ssh)
        elif task_obj.task_type == 'file_send':
            multi_call(paramiko_sftp)


def by_ansible(task_id):
    pass


def by_saltstack(task_id):
    pass


if __name__ == '__main__':
    # print(globals())
    try:
        opts, args = getopt(sys.argv[1:], 'i:t:')
        # i == task_id; t == run_type
    except GetoptError as e:
        print(e)
    else:
        # print(opts, args)
        arg_dic = {
            opt: val for opt, val in opts
        }
        if not re.match(r'\d+', arg_dic['-i']):
            raise TypeError('-i option require an integer type')
        func = globals()[arg_dic['-t']]
        # 如果全局变量不存在指定run_type将报一个字典key不存在的错误，此用法可减少一次判断
        func(arg_dic['-i'])
        # 将task_id作为参数传递给执行函数，告诉他你要去执行哪一条任务


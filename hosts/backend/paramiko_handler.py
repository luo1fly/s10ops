#!/usr/bin/env python
# Name: paramiko_handler.py
# Time:8/15/16 11:32 AM
# Author:luo1fly

import paramiko
import os
from django.utils import timezone
from s10ops import settings
from hosts import models
# import json
# from multiprocessing import Pool
# from multiprocessing import RLock
# import custom modules above


def paramiko_ssh(bind_host_to_user_ins, task_obj, task_id):
    print('going to run %s on %s' % (task_obj.cmd, bind_host_to_user_ins))
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if bind_host_to_user_ins.host_user.auth_type == 'ssh-password':
            conn_dic = dict(
                hostname=bind_host_to_user_ins.host.ip_address,
                username=bind_host_to_user_ins.host_user.username,
                password=bind_host_to_user_ins.host_user.password,
                port=bind_host_to_user_ins.host.port,
            )
            # print(conn_dic)
            ssh.connect(**conn_dic)
        else:
            # print(settings.RSA_PRIVATE_KEY_FILE)
            key = paramiko.RSAKey.from_private_key_file(settings.RSA_PRIVATE_KEY_FILE)
            conn_dic = dict(
                hostname=bind_host_to_user_ins.host.ip_address,
                port=bind_host_to_user_ins.host.port,
                username=bind_host_to_user_ins.host_user.username,
            )
            # print(conn_dic)
            ssh.connect(**conn_dic, pkey=key)
        stdin, stdout, stderr = ssh.exec_command(task_obj.cmd)
        result = (stdout.read().decode('utf8'), stderr.read().decode('utf8'))
        ssh.close()
        # print(result)
        # print(stdout.read(), stderr.read())
        itr_result = filter(lambda x: len(x) > 0, result)
        cmd_result = next(itr_result)
        # 注意此处filter函数的用法，元组元素对象的长度大于零，返回该元组对象的第一个元素，
        # 但在3.0版本返回的是满足条件的元素迭代器，需要用next方法来取值
        print('exe_result:%s' % cmd_result)
        result = 'success'
    except Exception as e:
        print("\033[31;1m%s\033[0m" % e.args[0])
        cmd_result = e
        result = 'failed'

    task_log_detail_obj = models.TaskLogDetail.objects.get(child_of_task_id=task_id,
                                                           bind_host_id=bind_host_to_user_ins.id)
    print('before:', task_log_detail_obj.result)
    task_log_detail_obj.result = result
    print('after:', task_log_detail_obj.result)
    task_log_detail_obj.event_log = cmd_result
    task_log_detail_obj.date = timezone.now()

    task_log_detail_obj.save()


def paramiko_sftp(bind_host_to_user_ins, task_obj, task_id):
    ts = paramiko.Transport((bind_host_to_user_ins.host.ip_address, bind_host_to_user_ins.host.port))
    try:
        if bind_host_to_user_ins.host_user.auth_type == 'ssh-password':
            ts.connect(
                username=bind_host_to_user_ins.host_user.username,
                password=bind_host_to_user_ins.host_user.password,
            )
        else:
            key = paramiko.RSAKey.from_private_key_file(settings.RSA_PRIVATE_KEY_FILE)
            ts.connect(
                username=bind_host_to_user_ins.host_user.username,
                pkey=key,
            )
        sftp = paramiko.SFTPClient.from_transport(ts)
        task_dic = eval(task_obj.cmd)
        # 此处用json.loads有问题，暂未查明

        if task_obj.task_type == 'file_send':
            upload_files = task_dic['upload_files']
            for file_path in upload_files:
                file_abs_path = "%s/%s/%s" % (settings.FileUploadDir, task_obj.user_id, file_path)
                print(file_abs_path)
                remote_filename = os.path.basename(file_path)
                print(
                    '---\033[32;1m sending [%s] to [%s]\033[0m' % (
                        remote_filename, task_dic['remote_path']
                    )
                )
                sftp.put(file_abs_path, "%s/%s" % (task_dic['remote_path'], remote_filename))
            cmd_result = "successfully send files %s to remote path [%s]" % (
                upload_files, task_dic['remote_path']
            )
            print(cmd_result)
            result = 'success'
    except Exception as e:
        cmd_result = e.args[0]
        result = 'failed'
    log_obj = models.TaskLogDetail.objects.get(child_of_task_id=task_id, bind_host_id=bind_host_to_user_ins.id)
    log_obj.event_log = cmd_result
    log_obj.date = timezone.now()
    log_obj.result = result
    log_obj.save()
#!/usr/bin/env python
# Name: task.py
# Time:8/11/16 10:23 AM
# Author:luo1fly


class Task(object):
    def __init__(self, request):
        self.request = request

    def call(self, task_type):
        func = getattr(self, task_type)
        return func()

    def multi_cmd(self):
        print('---going to run cmd----', self.request.POST['task_type'])

    def multi_file_transfer(self):
        pass

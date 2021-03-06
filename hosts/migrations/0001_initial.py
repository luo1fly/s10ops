# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-24 03:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=64, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=32)),
                ('token', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='token')),
                ('department', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='部门')),
                ('tel', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='座机')),
                ('mobile', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='手机')),
                ('memo', models.TextField(blank=True, default=None, null=True, verbose_name='备注')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('valid_begin_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_end_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': '用户信息',
                'verbose_name': '用户信息',
            },
        ),
        migrations.CreateModel(
            name='BindHostToUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': '主机与用户绑定关系',
                'verbose_name': '主机与用户绑定关系',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('ip_address', models.GenericIPAddressField(unique=1)),
                ('port', models.IntegerField(default=22)),
                ('system_type', models.CharField(choices=[('linux', 'Linux'), ('windows', 'Windows')], default='linux', max_length=32)),
                ('enabled', models.BooleanField(default=1)),
                ('memo', models.TextField(blank=1, null=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '远程主机',
                'verbose_name': '远程主机',
            },
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=1)),
                ('memo', models.TextField(blank=1, null=1)),
            ],
            options={
                'verbose_name_plural': '主机组',
                'verbose_name': '主机组',
            },
        ),
        migrations.CreateModel(
            name='HostUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_type', models.CharField(choices=[('ssh-password', 'SSH/PASSWORD'), ('ssh-key', 'SSH/KEY')], default='ssh-password', max_length=32)),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(blank=1, max_length=128, null=1)),
            ],
            options={
                'verbose_name_plural': '远程主机用户',
                'verbose_name': '远程主机用户',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=1)),
                ('memo', models.TextField(blank=1, null=1)),
            ],
            options={
                'verbose_name_plural': '数据中心',
                'verbose_name': '数据中心',
            },
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('task_type', models.CharField(choices=[('multi_cmd', 'CMD'), ('file_send', '批量发送文件'), ('file_get', '批量下载文件')], max_length=50)),
                ('cmd', models.TextField()),
                ('expire_time', models.IntegerField(default=30)),
                ('task_pid', models.IntegerField(default=0)),
                ('note', models.CharField(blank=True, max_length=100, null=True)),
                ('hosts', models.ManyToManyField(to='hosts.BindHostToUser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '批量任务',
                'verbose_name': '批量任务',
            },
        ),
        migrations.CreateModel(
            name='TaskLogDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('event_log', models.TextField()),
                ('result', models.CharField(choices=[('success', 'Success'), ('failed', 'Failed'), ('unknown', 'Unknown')], default='unknown', max_length=30)),
                ('note', models.CharField(blank=True, max_length=100)),
                ('bind_host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosts.BindHostToUser')),
                ('child_of_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosts.TaskLog')),
            ],
            options={
                'verbose_name_plural': '批量任务日志',
                'verbose_name': '批量任务日志',
            },
        ),
        migrations.AlterUniqueTogether(
            name='hostuser',
            unique_together=set([('auth_type', 'username', 'password')]),
        ),
        migrations.AddField(
            model_name='host',
            name='idc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosts.IDC'),
        ),
        migrations.AddField(
            model_name='bindhosttouser',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosts.Host'),
        ),
        migrations.AddField(
            model_name='bindhosttouser',
            name='host_groups',
            field=models.ManyToManyField(to='hosts.HostGroup'),
        ),
        migrations.AddField(
            model_name='bindhosttouser',
            name='host_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosts.HostUser'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bind_hosts',
            field=models.ManyToManyField(blank=1, to='hosts.BindHostToUser'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='host_groups',
            field=models.ManyToManyField(blank=1, to='hosts.HostGroup'),
        ),
        migrations.AlterUniqueTogether(
            name='bindhosttouser',
            unique_together=set([('host', 'host_user')]),
        ),
    ]

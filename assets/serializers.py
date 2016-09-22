#!/usr/bin/env python
# Name: serializers.py
# Time:8/24/16 2:29 PM
# Author:luo1fly

from rest_framework import serializers
from django.contrib.auth.models import Group
from hosts.models import UserProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('url', 'name', 'email',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name',)

#!/usr/bin/env python
# Name: rest_views.py
# Time:8/24/16 2:37 PM
# Author:luo1fly

from assets.serializers import UserSerializer, GroupSerializer
from rest_framework import viewsets
from hosts.models import UserProfile
from django.contrib.auth.models import Group


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

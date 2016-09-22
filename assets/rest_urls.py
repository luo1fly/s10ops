#!/usr/bin/env python
# Name: rest_urls.py
# Time:8/24/16 2:44 PM
# Author:luo1fly

from rest_framework import routers
from assets import rest_views
from django.conf.urls import url, include

router = routers.DefaultRouter()
router.register(r'users', rest_views.UserViewSet)
router.register(r'groups', rest_views.GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
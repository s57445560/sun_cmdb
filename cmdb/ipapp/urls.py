#!/usr/bin/env python
# coding:utf-8
# Author: Sun Yang

from django.conf.urls import url, include
from django.contrib import admin

from ipapp import views


urlpatterns = [
    url(r'^home/$', views.home),
    url(r'^auth_login/$', views.auth_login),
    url(r'^logout/', views.logout),
    url(r'^add/', views.add),
    # url(r'^modify/', views.modify),
    url(r'^select/', views.select),
    url(r'^auth_register/', views.auth_register),
    url(r'^modify/(?P<p1>\d+)/', views.modify),


]
"""ops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from .views import *

urlpatterns = [
    re_path(r'idcs/(?P<pk>\d+)?/?$', IdcView.as_view()),
    re_path(r'api_idc/(?P<pk>\d+)?/?$', ApiIdcs.as_view()),
    re_path(r'racks/(?P<pk>\d+)?/?$', RackView.as_view()),
    re_path(r'api_rack/(?P<pk>\d+)?/?$', ApiRack.as_view()),
    re_path(r'servers/(?P<pk>\d+)?/?$', ServerView.as_view()),
    re_path(r'api_count/(?P<pk>\d+)?/?$', ApiCount.as_view()),
    re_path(r'reporting/(?P<pk>\d+)?/?$', Reporting.as_view()),
]

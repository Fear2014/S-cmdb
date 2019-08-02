from django.urls import path,re_path
from .views import *

urlpatterns = [
    re_path(r'dbconf/(?P<pk>\d+)?/?$', DBConf.as_view()),
    re_path(r'inception_check/$', Inception_Check.as_view()),
    re_path(r'API_DB_env/$', API_DB_env.as_view()),
    re_path(r'inception_list/(?P<pk>\d+)?/?$', Inception_list.as_view()),
    re_path(r'Api_Cancel/(?P<pk>\d+)?/?$', Api_Cancel.as_view()),

]
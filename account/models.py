from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role={
        (1, u'总监'),
        (1, u'经理'),
        (1, u'开发')
    }
    nick_name = models.TextField(max_length=64, blank=True) # 扩展字段
    location = models.CharField(max_length=32, blank=True) # 扩展字段
    birth_date = models.DateField(null=True, blank=True) # 扩展字段
    roles = models.CharField(max_length=32, blank=True, choices=role) # 扩展字段
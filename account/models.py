from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nick_name = models.TextField(max_length=64, blank=True) # 扩展字段
    location = models.CharField(max_length=32, blank=True) # 扩展字段
    birth_date = models.DateField(null=True, blank=True) # 扩展字段
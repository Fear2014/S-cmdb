from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class BaseModel(models.Model):
    name = models.CharField(max_length=32)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    remark = models.TextField()

    class Meta:
        abstract = True
        ordering = ['id']
        unique_together = ('name',)
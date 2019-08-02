from django.db import models
from django.contrib.auth.models import User
from account.models import User
from utils.basemodel import BaseModel

class DBConf(BaseModel):
    ENV = {
        (1, u'测试'),
        (2, u'生产')
    }
    user = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    port = models.CharField(max_length=8)
    env = models.IntegerField(choices=ENV)

    @property
    def to_dict(self):
        res = {}
        filds = [f.name for f in self._meta.fields]
        for fild in filds:
            value = getattr(self, fild, None)
            res[fild] = value
        if res.get('env') == 1:
            res['env_name'] = '测试'
        elif res.get('env') == 2:
            res['env_name'] = '生产'
        else:
            res['env_name'] = ''
        return res


class InpectionSql(models.Model):
    STATUS = {
        (-3, u'回滚失败'),
        (-2, u'回滚成功'),
        (-1, u'待执行'),
        (0, u'执行成功'),
        (1, u'已放弃'),
        (2, u'执行失败'),
    }
    sql_user = models.ManyToManyField(User)
    commiter = models.CharField(max_length=128)
    sql_conent = models.TextField()
    env = models.CharField(max_length=16)
    db_name = models.CharField(max_length=48)
    treater = models.CharField(max_length=128)
    status = models.IntegerField(choices=STATUS, default='-1')
    exe_affected_rows = models.CharField(max_length=32)
    rollback_id = models.CharField(max_length=128)
    rollback_db = models.CharField(max_length=128)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    remark = models.TextField()

    @property
    def to_dict(self):
        res = {}
        filds = [f.name for f in self._meta.fields]
        for fild in filds:
            value = getattr(self, fild, None)
            res[fild] = value
        return res


def __str__(self):
    return self.name
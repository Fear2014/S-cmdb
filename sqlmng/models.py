from django.db import models
from django.contrib.auth.models import User
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



def __str__(self):
    return self.name
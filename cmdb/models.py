from django.db import models
from django.contrib.auth.models import User
from utils.basemodel import BaseModel

class Idc(BaseModel):
    address = models.CharField(max_length=100)
    price = models.CharField(max_length=64, null=True, blank=True, default='0')

    @property
    def name_handle(self):
        return '江苏_' + self.name

    @property
    def to_dict(self):
        res = {}
        filds = [ f.name for f in self._meta.fields]
        for fild in filds:
            value = getattr(self, fild, None)
            res[fild] = value
        racks = self.IDC_RACK.all()
        res['rack'] = {'count': racks.count(), 'data': [obj for obj in racks.values()]}
        #res['name'] = '*' +res.get('name')[1:len(res['name'])-2]+ '*'*2
        #res.pop('price')
        return res





class Rack(BaseModel):
    idc = models.ForeignKey(Idc, on_delete=models.SET_NULL, null=True, related_name='IDC_RACK')
    numb = models.CharField(max_length=32, null=True, blank=True)
    size = models.CharField(max_length=32, null=True, blank=True)

    @property
    def to_dict(self):
        res = {}
        filds = [f.name for f in self._meta.fields]
        for fild in filds:
            value = getattr(self, fild, None)
            res[fild] = value
        obj = getattr(self, 'idc')
        res['idc'] = {'id': obj.id, 'name': obj.name } if obj else {}
        servers = self.RACK_SEVER.all()
        res['server'] = {'count': servers.count(), 'data': [server for server in servers.values()] }
        return res


class Server(BaseModel):
    STATUS = (
        (0, u'下线'),
        (1, u'在线'),
    )

    rack = models.ForeignKey(Rack, on_delete=models.SET_NULL, null=True, blank=True, related_name='RACK_SEVER', verbose_name='所属机柜')
    uuid = models.CharField( max_length=128, default='', null=True, blank=True, verbose_name='UUID')
    cpu = models.CharField(max_length=64,  default='', null=True, blank=True, verbose_name='CPU')
    memory = models.CharField(max_length=64, default='', null=True, blank=True, verbose_name='内存')
    disk = models.CharField(max_length=64, default='', null=True, blank=True, verbose_name='磁盘')
    ip = models.CharField(max_length=64, default='', null=True, blank=True, verbose_name='IP')
    business = models.CharField(max_length=64, default='', null=True, blank=True, verbose_name='业务线')
    server_type = models.CharField(max_length=128, default='', null=True, blank=True, verbose_name='服务器类型')
    daq = models.TextField(default='', null=True, blank=True, verbose_name='数据采集')
    status = models.IntegerField(default=1, choices=STATUS, verbose_name='运行状态')


    @property
    def to_dict(self):
        res = {}
        filds = [f.name for f in self._meta.fields]
        for fild in filds:
            value = getattr(self, fild, None)
            res[fild] = value
        obj = getattr(self, 'rack')
        daq1 = eval(self.daq) if self.daq else ''
        res['daq1'] = daq1
        res['rack'] = {'id': obj.id, 'name': obj.name} if obj else {}
        return res


def __str__(self):
    return self.name
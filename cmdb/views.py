from django.db.models import Q
from .models import *
from utils.baseview import BaseCmdbApi, BaseListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.http import JsonResponse, QueryDict

class Reporting(View):
    def post(self, request, *args, **kwargs):
        get_data = QueryDict(request.body).dict()
        hostname = get_data.get('hostname')
        cpu = get_data.get('server_cpu')
        memory = get_data.get('server_mem')
        disk = get_data.get('server_disk').split('\"')[1]
        ip = eval(get_data.get('ipinfo'))[0].get('ip')
        mac = eval(get_data.get('ipinfo'))[0].get('mac')
        uuid = get_data.get('uuid')
        server_type = get_data.get('server_type')
        daq = {'mac': mac, 'manufacturers': mac+get_data.get('manufacturers'), 'st': get_data.get('st'), 'manufacture_date': get_data.get('manufacture_date'), 'os': get_data.get('os'), 'vm_status': get_data.get('vm_status')}
        data = {'name': hostname, 'cpu': cpu, 'memory': memory, 'disk': disk, 'ip': ip, 'uuid': uuid, 'server_type': server_type, 'daq': daq}
        if Server.objects.filter(uuid=uuid, server_type=server_type):
            Server.objects.filter(uuid=uuid, server_type=server_type).update(**data)
        else:
            Server.objects.create(**data)
        return JsonResponse({})


class ApiIdcs(BaseCmdbApi):
    model = Idc



class ApiRack(BaseCmdbApi):
    model = Rack

class ApiCount(View):

    def get(self, request, *args, **kwargs):
        idcs_count = Idc.objects.all().count()
        racks_count = Rack.objects.all().count()
        servers_count = Server.objects.all().count()
        count = {
            'idcs_count': idcs_count,
            'racks_count': racks_count,
            'servers_count': servers_count
        }
        total = []
        idc_chart_datas = []
        chart_datas = []     #饼图参数
        for idc in Idc.objects.all():
            servers_numb = 0
            rack_numb = idc.IDC_RACK.count()
            for rack in idc.IDC_RACK.all():
                server_numb = rack.RACK_SEVER.count()
                servers_numb += server_numb
            res = {'idc_name': idc.name, 'idc_rack_numb': rack_numb*10, 'servers_numb':  servers_numb}
            total.append(res)
            idc_chart_data = [idc.name, servers_numb]
            idc_chart_datas.append(idc_chart_data)
        chart_datas.append({
                  'type': 'pie',
                  'name': 'Browser share',
                  'data': idc_chart_datas
                })
        data = {'count':count, 'total':total, 'chart_datas': chart_datas}

        return JsonResponse(data)

class IdcView(BaseListView):
    model = Idc
    template_name = 'cmdb/idcs.html'
    template_detial = 'cmdb/idc_detial.html'


    def get_queryset(self):
        queryset = self.model.objects.all().order_by('id')
        search = self.request.GET.get('search')
        if search:
            queryset = self.model.objects.filter(Q(name__icontains=search) | Q(address__icontains=search)).order_by('id')
        queryset = [obj.to_dict for obj in queryset]
        return queryset


class RackView(BaseListView):
    model = Rack
    paginator_numb = 3
    template_name = 'cmdb/rack.html'
    template_detial = 'cmdb/rack_detial.html'


    def get_queryset(self):
        queryset = self.model.objects.all().order_by('id')
        search = self.request.GET.get('search')
        idc_id = self.request.GET.get('idc_id')
        if idc_id:
            queryset = self.model.objects.filter(idc_id=idc_id).order_by('id')
        if search:
            queryset = self.model.objects.filter(Q(name__icontains=search) | Q(size__icontains=search)).order_by('id')
        queryset = [obj.to_dict for obj in queryset]
        return queryset


class ServerView(BaseListView):
    model = Server
    template_name = 'cmdb/server.html'
    template_detial = 'cmdb/server_detial.html'
    def get_queryset(self):
        queryset = self.model.objects.all().order_by('id')
        search = self.request.GET.get('search')
        rack_id = self.request.GET.get('rack_id')
        if rack_id:
            queryset = self.model.objects.filter(rack_id=rack_id).order_by('id')
        if search:
            queryset = self.model.objects.filter(Q(name__icontains=search) | Q(server_type__icontains=search)).order_by('id')
        queryset = [obj.to_dict for obj in queryset]
        return queryset

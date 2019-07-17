from django.shortcuts import render
from django.views.generic import View,TemplateView,ListView
from django.http import JsonResponse,HttpResponse,QueryDict
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.baseview import BaseListView
from utils.wrappers import handle_data_check
# Create your views here.

class ApiIdcs(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            idcs_data = Idc.objects.get(id=pk)
            data = {'data': idcs_data.to_dict}
        else:
            idcs_data = Idc.objects.all()
            data = {'data': [idcs.to_dict for idcs in idcs_data]}
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

    @handle_data_check
    #@permission_required(' cmdb.add_idc ')
    def post (self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        print(data)
        self.model.objects.create(**data)
        return JsonResponse({'status': '0'})

    def delete (self, request, *args, **kwargs):
        data = kwargs.get('pk')
        self.model.objects.get(id=data).delete()
        return JsonResponse({})

    @handle_data_check
    def put (self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        self.model.objects.filter(id=pk).update(**data)
        return JsonResponse({'status': '0'})


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

    @handle_data_check
    def post (self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        self.model.objects.create(**data)
        return JsonResponse({'status': '0'})

    def delete (self, request, *args, **kwargs):
        data = kwargs.get('pk')
        self.model.objects.get(id=data).delete()
        return JsonResponse({'status': '0'})

    @handle_data_check
    def put (self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        self.model.objects.filter(id=pk).update(**data)
        return JsonResponse({'status': '0'})



class ApiRack(LoginRequiredMixin, View):
    model = Rack

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            obj_data = self.model.objects.get(id=pk)
            data = {'data': obj_data.to_dict}
        else:
            obj_data = self.model.objects.all()
            data = {'data': [obj.to_dict for obj in obj_data]}
        return JsonResponse(data)



class ServerView(BaseListView):
    model = Server
    template_name = 'cmdb/server.html'

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

    @handle_data_check
    def post (self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        self.model.objects.create(**data)
        return JsonResponse({'status': '0'})

    def delete (self, request, *args, **kwargs):
        data = kwargs.get('pk')
        self.model.objects.get(id=data).delete()
        return JsonResponse({'status': '0'})

    @handle_data_check
    def put (self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        self.model.objects.filter(id=pk).update(**data)
        return JsonResponse({'status': '0'})
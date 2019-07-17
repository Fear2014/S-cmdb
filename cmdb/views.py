from django.shortcuts import render
from django.views.generic import View,TemplateView,ListView
from django.http import JsonResponse,HttpResponse,QueryDict
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
'''
class IdcView(TemplateView):
    template_name = 'cmdb/idcs.html'

    def get_context_data(self, **kwargs):
        idcs = Idc.objects.all()
        return {'idcs':idcs}
'''


def servers(request):
    server_list = Server.objects.all()
    paginator = Paginator(server_list,2,0)
    page = request.GET.get('page')
    try:
        paginator_data = paginator.page(page)
    except PageNotAnInteger:
        paginator_data = paginator.page(1)
    except EmptyPage:
        paginator_data = paginator.page(paginator.num_pages)
    return render(request, 'cmdb/server.html', {'paginator_data':paginator_data})

class ApiIdcs(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            idcs_data = Idc.objects.get(id=pk)
            data = {'data': idcs_data.to_dict}
        else:
            idcs_data = Idc.objects.all()
            data = {'data': [idcs.to_dict for idcs in idcs_data]}
        return JsonResponse(data)



class IdcView(LoginRequiredMixin, ListView):
    model = Idc
    template_name = 'cmdb/idcs.html'
    template_detial = 'cmdb/idc_detial.html'


    def handle_page(self, queryset, page):
        paginator = Paginator(queryset, 10, 5)
        try:
            paginator_data = paginator.page(page)
        except PageNotAnInteger:
            paginator_data = paginator.page(1)
        except EmptyPage:
            paginator_data = paginator.page(paginator.num_pages)
        return paginator_data


    def get (self, request, *args, **kwargs):
        queryset = self.model.objects.all().order_by('id')
        pk = kwargs.get('pk')
        print(pk)
        if pk:
            paginator_data = self.model.objects.get(pk=pk)
            return render(request, self.template_detial, paginator_data.to_dict)

        page = request.GET.get('page')
        search = request.GET.get('search')

        if search:
            queryset = self.model.objects.filter(Q(name__icontains=search) | Q(address__icontains=search)).order_by('id')
        queryset = [obj.to_dict for obj in queryset]
        paginator_data = self.handle_page(queryset, page)
        return render(request, self.template_name, {'paginator_data': paginator_data})

    #@permission_required(' cmdb.add_idc ')
    def post (self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        print(data)
        self.model.objects.create(**data)
        return JsonResponse({'status': '1'})

    def delete (self, request, *args, **kwargs):
        data = kwargs.get('pk')
        self.model.objects.get(id=data).delete()
        return JsonResponse({})

    def put (self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        self.model.objects.filter(id=pk).update(**data)
        return JsonResponse({})


class RackView(LoginRequiredMixin, ListView):
    model = Rack
    template_name = 'cmdb/rack.html'
    template_detial = 'cmdb/rack_detial.html'

    def handle_page(self, queryset, page):
        paginator = Paginator(queryset, 3, 0)
        try:
            paginator_data = paginator.page(page)
        except PageNotAnInteger:
            paginator_data = paginator.page(1)
        except EmptyPage:
            paginator_data = paginator.page(paginator.num_pages)
        return paginator_data




    def get (self, request, *args, **kwargs):
        queryset = self.model.objects.all().order_by('id')
        page = request.GET.get('page')
        search = request.GET.get('search')
        idc_id = request.GET.get('idc_id')
        pk = kwargs.get('pk')
        if pk:
            queryset = self.model.objects.get(pk=pk)
            return render(request, self.template_detial, queryset.to_dict)
        if idc_id:
            queryset = self.model.objects.filter(idc_id=idc_id).order_by('id')
        if search:
            queryset = self.model.objects.filter(Q(name__icontains=search) | Q(size__icontains=search)).order_by('id')
        queryset = [obj.to_dict for obj in queryset]
        paginator_data = self.handle_page(queryset, page)
        return render(request, self.template_name, {'paginator_data': paginator_data})

    def post (self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        self.model.objects.create(**data)
        return JsonResponse({'status': '1'})

    def delete (self, request, *args, **kwargs):
        data = kwargs.get('pk')
        self.model.objects.get(id=data).delete()
        return JsonResponse({})

    def put (self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        self.model.objects.filter(id=pk).update(**data)
        return JsonResponse({})



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



class ServerView(LoginRequiredMixin, ListView):
    model = Server
    template_name = 'cmdb/server.html'

    def handle_page(self, queryset, page):
        paginator = Paginator(queryset, 3, 0)
        try:
            paginator_data = paginator.page(page)
        except PageNotAnInteger:
            paginator_data = paginator.page(1)
        except EmptyPage:
            paginator_data = paginator.page(paginator.num_pages)
        return paginator_data




    def get (self, request, *args, **kwargs):
        queryset = self.model.objects.all().order_by('id')
        page = request.GET.get('page')
        search = request.GET.get('search')
        rack_id = request.GET.get('idc_id')
        if rack_id:
            queryset = self.model.objects.filter(rack_id=rack_id).order_by('id')
        if search:
            queryset = self.model.objects.filter(Q(name__icontains=search) | Q(server_type__icontains=search)).order_by('id')
        queryset = [obj.to_dict for obj in queryset]
        paginator_data = self.handle_page(queryset, page)
        return render(request, self.template_name, {'paginator_data': paginator_data})

    def post (self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        self.model.objects.create(**data)
        return JsonResponse({'status': '1'})

    def delete (self, request, *args, **kwargs):
        data = kwargs.get('pk')
        self.model.objects.get(id=data).delete()
        return JsonResponse({})

    def put (self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        self.model.objects.filter(id=pk).update(**data)
        return JsonResponse({})
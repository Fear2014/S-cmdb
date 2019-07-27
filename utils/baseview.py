from django.shortcuts import render
from django.views.generic import ListView, View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.wrappers import handle_data_check
from django.http import JsonResponse, QueryDict


class BaseCmdbApi(LoginRequiredMixin, View):
    model = None

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            obj_data = self.model.objects.get(id=pk)
            data = {'data': obj_data.to_dict}
        else:
            obj_data = self.model.objects.all()
            data_count = obj_data.count()
            print(data_count)
            data = {'data_count': data_count, 'data': [obj.to_dict for obj in obj_data]}
        return JsonResponse(data)


class BaseListView(LoginRequiredMixin, ListView):
    model = None
    template_detial = None
    paginator_numb = 10

    def handle_page(self, queryset, page):
        paginator = Paginator(queryset, self.paginator_numb, 0)
        pagecount = paginator.num_pages
        try:
            paginator_data = paginator.page(page)
        except PageNotAnInteger:
            paginator_data = paginator.page(1)
        except EmptyPage:
            paginator_data = paginator.page(paginator.num_pages)
        data = {'paginator_data': paginator_data, 'page_count': pagecount}
        return data

    def get (self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        page = request.GET.get('page')
        #详情页
        if pk:
            paginator_data = self.model.objects.get(pk=pk)
            return render(request, self.template_detial, paginator_data.to_dict)
        #列表页
        queryset = self.get_queryset()
        search = self.request.GET.get('search', '')
        paginator_data = self.handle_page(queryset, page).get('paginator_data')
        page_count = self.handle_page(queryset, page).get('page_count')
        return render(request, self.template_name, {'paginator_data': paginator_data, 'search': search, 'page_count': page_count})


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
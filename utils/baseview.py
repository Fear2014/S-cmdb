from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin

class BaseListView(LoginRequiredMixin, ListView):
    model = None
    template_detial = None
    paginator_numb = 2

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
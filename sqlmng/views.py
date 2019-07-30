from utils.baseview import BaseListView
from django.db.models import Q
from django.views.generic import TemplateView, View
from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from .models import *
class DBConf(BaseListView):
    model = DBConf
    template_name = 'sqlmng/dbconf.html'

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('id')
        search = self.request.GET.get('search')
        if search:
            queryset = self.model.objects.filter(Q(name__icontains=search) | Q(address__icontains=search)).order_by('id')
        queryset = [obj.to_dict for obj in queryset]
        return queryset

class Inception_Check(TemplateView):
    template_name = 'sqlmng/inception_check.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        print(data)
        return JsonResponse({})


class API_DB_env(View):
    def post(self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        user = request.user
        env = data.get('env')
        queryset = DBConf.model.objects.filter(env=env)
        queryset = [obj.to_dict for obj in queryset]
        print(user)
        return JsonResponse({'data': queryset, 'user': str(user)})







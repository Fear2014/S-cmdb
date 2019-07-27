from utils.baseview import BaseListView
from django.db.models import Q
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






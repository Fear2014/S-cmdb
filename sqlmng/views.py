from utils.baseview import BaseListView
from django.db.models import Q
from django.views.generic import TemplateView, View
from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from .models import *
from utils.inception_tools import inception_tools
from account.models import User

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
        user = request.user
        env = data.get('env')
        sql_conent = data.get('sql_conent')
        db_name = data.get('db_name')
        treater = data.get('treater')
        remark = data.get('remark')
        db = DBConf.model.objects.get(env=env, name=db_name)
        db_user = db.user
        db_password= db.password
        db_host = db.address
        port = db.port
        data = {'user': db_user, 'password': db_password, 'host': db_host, 'port': port, 'db_name': db_name, 'sql_conent': sql_conent}
        status, result = inception_tools(data)
        if status == 1:
            return JsonResponse({'status': status, 'result': result})
        else:
            result = result[1]
            exe_affected_rows = result[6]
            rollback_id = result[7]
            rollback_db = result[8]
            print(env)
            if env == '1':
                env = '测试环境'
            else:
                env = '生产环境'
            data = {'commiter': str(user), 'sql_conent': sql_conent, 'env': env, 'db_name': db_name, 'treater': treater, \
                    'exe_affected_rows': exe_affected_rows, 'rollback_id': rollback_id, 'rollback_db': rollback_db, \
                    'remark': remark, 'status': '-1'}
            print(data)
            obj = InpectionSql.objects.create(**data)
            treater_obj = User.objects.get(username=treater)
            obj.sql_user.add(user, treater_obj)
            return JsonResponse({'status': status, 'result': result})




class Inception_list(BaseListView):
    model = InpectionSql
    template_name = 'sqlmng/inception_list.html'

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('id')
        search = self.request.GET.get('search')
        if search:
            queryset = self.model.objects.filter(Q(commiter__icontains=search) | Q(env__icontains=search)).order_by('id')
        queryset = [obj.to_dict for obj in queryset]
        return queryset




class API_DB_env(View):
    def post(self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        user = request.user
        env = data.get('env')
        if str(user) == 'admin':
            treaters = [str(user)]
        else:
            if env == '1':
                treaters = [str(user)]
            if env == '2':
                user_obj = User.objects.get(username=str(user))
                role = user_obj.roles
                if role == '3':
                    treater_query = User.objects.filter(roles='2')
                    treaters = [treater_obj.username for treater_obj in treater_query]
                if role == '2':
                    treater_query = User.objects.filter(roles='1')
                    treaters = [treater_obj.username for treater_obj in treater_query]
                if role == '1':
                    treaters = [str(user)]
        queryset = DBConf.model.objects.filter(env=env)
        queryset = [obj.to_dict for obj in queryset]
        return JsonResponse({'data': queryset, 'user': treaters})


class Api_Cancel(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        data = {'status': 1}
        obj = InpectionSql.objects.get(id=pk)
        obj.status = 1
        obj.save()
        return JsonResponse({})






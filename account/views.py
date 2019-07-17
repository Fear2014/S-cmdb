# -*- coding: utf-8 -*-
from django.views.generic import View, TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(TemplateView):
    template_name = 'login.html'
    error_msg = ''
    def post(self, request, *args, **kwargs):
        username = request.POST.get('User')
        password = request.POST.get('Password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            error_msg = '用户名/密码不对'
        return render(request, self.template_name, {'error_msg': error_msg})
        #return render(request, self.template_name, {'status': status})

class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/account/login/')


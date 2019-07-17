# -*- coding: utf-8 -*-
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexPage(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


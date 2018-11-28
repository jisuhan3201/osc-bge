from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . import models


class SecondaryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, secondary_id=None):


        return render(request, 'school/test.html', {})

class SecondaryLogView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, secondary_id=None):


        return render(request, 'school/testlog.html', {})

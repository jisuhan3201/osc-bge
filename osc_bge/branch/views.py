from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.

class BranchStatisticsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'branch/statistics.html', {})


class BranchSecondaryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'branch/secondary.html', {})


class BranchStudentsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'branch/students.html', {})


class BranchHostsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'branch/hosts.html', {})


class BranchResourcesView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    
    def get(self, request):

        return render(request, 'branch/resources.html', {})

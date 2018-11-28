from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


@login_required(login_url='/accounts/login/')
def index(request):

    if request.user.type == 'counseler':

        return redirect('/agent/counsel')

    elif request.user.type == 'agency_admin':
        return redirect('/agent/statistics')

    else:
        return redirect('/statistics')


class BgeStatisticsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'main/statistics.html', {})


class BranchesView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'main/branches.html', {})


class AgentsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'main/agents.html', {})


class SecondaryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'main/secondary.html', {})

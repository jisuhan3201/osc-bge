from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def index(request):

    if request.user.type == 'counseler':

        return redirect('/agent/statistics')

    else:
        return redirect('/agent/process')

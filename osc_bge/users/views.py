from django.http import *
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def login_success(request):

    if request.user.is_authenticated:

        if request.user.type == "counseler":

            return redirect('/agent/prospective')

        else:
            return redirect('/agent/statistics')

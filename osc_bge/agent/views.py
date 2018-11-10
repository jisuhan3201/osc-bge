from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from . import models
from osc_bge.users import models as user_models

class CounselView(View):

    def get(self, request):

        return render(request, 'agent/counsel.html', {})


class RegisterView(View):

    def get(self, request):

        return render(request, 'agent/register.html', {})

    def post(self, request):

        user = request.user
        data = request.POST
        print(data)
        return HttpResponse(status=202)

def statistics(request):

    return render(request, 'agent/statistics.html', {})

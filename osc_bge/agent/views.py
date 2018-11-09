from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from . import models

class CounselView(View):

    def get(self, request):

        return render(request, 'agent/counsel.html', {})


def statistics(request):

    return render(request, 'agent/statistics.html', {})

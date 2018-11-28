from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . import models


class SecondaryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, secondary_id=None):

        try:
            found_secondary = models.Secondary.objects.get(pk=secondary_id)
        except models.Secondary.DoesNotExist:
            return HttpResponse(status=400)

        return render(request, 'school/secondary.html', {
            "found_secondary":found_secondary,
        })

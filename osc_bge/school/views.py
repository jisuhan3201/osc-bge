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


class CollegeSchoolView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, secondary_id=None):


        return render(request, 'school/college.html', {})


class SecondarySummaryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, secondary_id=None):


        return render(request, 'school/summary.html', {})


class SecondaryDetailView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, secondary_id=None):


        return render(request, 'school/detailed_info.html', {})


class SecondaryServiceView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, secondary_id=None):


        return render(request, 'school/service.html', {})


class SecondaryReviewView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, secondary_id=None):


        return render(request, 'school/review.html', {})


class SecondaryEstimateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, secondary_id=None):


        return render(request, 'school/estimate.html', {})


class SecondaryPhotoView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, secondary_id=None):


        return render(request, 'school/photo.html', {})

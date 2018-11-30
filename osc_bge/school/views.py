from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . import models, forms
from osc_bge.users import models as user_models
from osc_bge.bge import models as bge_models


class SecondaryCreateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'school/create.html', {})

    def post(self, request):

        data = request.POST
        print(data)
        print(request.FILES)
        if data.get('provider_branch'):
            try:
                found_branch = bge_models.BgeBranch.objects.get(pk=int(data.get('provider_branch')))
            except bge_models.BgeBranch.DoesNotExist:
                return HttpResponse(status=400)
        else:
            found_branch = None

        if data.get('admission_coordi'):
            try:
                found_admission_coordi = user_models.BgeBranchCoordinator.objects.get(pk=int(data.get('admission_coordi')))
            except user_models.BgeBranchCoordinator.DoesNotExist:
                return HttpResponse(status=400)
        else:
            found_admission_coordi = None

        if data.get('school_coordi'):
            try:
                found_school_coordi = user_models.BgeBranchCoordinator.objects.get(pk=int(data.get('admission_coordi')))
            except user_models.BgeBranchCoordinator.DoesNotExist:
                return HttpResponse(status=400)
        else:
            found_school_coordi = None

        if request.FILES.get('image'):
            form = forms.ImageUploadForm(request.FILES.get('image'))
            if form.is_valid():
                uploaded_image = form.cleaned_data.get('image')
            else:
                uploaded_image = None
        else:
            uploaded_image = None

        school = models.School(
            name = data.get('name'),
            type = 'secondary',
            image = uploaded_image if uploaded_image else None,
            partnership = int(data.get('partnership')) if data.get('partnership') else None,
            provider = data.get('provider'),
            provider_branch = found_branch,
            admission_coordi = found_admission_coordi,
            school_coordi = found_school_coordi,
            term = data.get('term'),
            transfer = True if data.get('transfer') else False,
            country = data.get('country'),
            address = data.get('address'),
            area_description = data.get('area_description'),
            phone = data.get('phone'),
            web_url = data.get('web_url'),
            founded = data.get('founded'),
            religion = data.get('religion'),
            number_students = int(data.get('number_students')) if data.get('number_students') else None,
        )
        school.save()

        secondary = models.Secondary(
            school=school,
            grade_start = int(data.get('grade_start')) if data.get('grade_start') else None,
            grade_end = int(data.get('grade_end')) if data.get('grade_end') else None,
            accept_12_grade = True if data.get('accept_12_grade') else False,
            application_fee = int(data.get('application_fee')) if data.get('application_fee') else None,
            program_fee = int(data.get('program_fee')) if data.get('program_fee') else None,
            admission_requirements = data.get('admission_requirements'),
            admission_documents = data.get('admission_documents'),
            selling_point = data.get('selling_point'),
            state = data.get('state'),
            student_body = data.get('student_body'),
            international_students = int(data.get('international_students')) if data.get('international_students') else None,
            esl = True if data.get('esl') else False,
            student_teach_ratio = data.get('student_teach_ratio'),
            class_size = data.get('class_size'),
            uniform = True if data.get('uniform') else False,
            college_acceptance_rate = data.get('college_acceptance_rate'),
            avg_sat = data.get('avg_sat'),
            number_honor_courses = data.get('number_honor_courses'),
            list_honor_courses = data.get('list_honor_courses'),
            number_ap_courses = data.get('number_ap_courses'),
            list_ap_courses = data.get('list_ap_courses'),
            number_clubs = data.get('number_clubs'),
            number_sports = data.get('number_sports'),
            facilities = data.get('facilities'),
        )
        secondary.save()

        if data.get('school_type'):

            for school_type in data.getlist('school_type'):
                school_types = models.SchoolTypes(
                    school = school,
                    type = school_type,
                )
                school_types.save()

        if request.FILES.get('photo'):

            for photo in request.FILES.get('photo'):
                form = forms.ImageUploadForm(photo)
                if form.is_valid():
                    uploaded_image = form.cleaned_data.get('image')
                else:
                    uploaded_image = None

                school_photo = models.SchoolPhotos(
                    school = school,
                    photo = uploaded_image,
                )
                school_photo.save()

        return redirect('/branch/secondary')


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

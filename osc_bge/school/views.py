from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . import models, forms
from osc_bge.users import models as user_models
from osc_bge.bge import models as bge_models
from osc_bge.student import models as student_models


class SecondaryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        all_schools = models.School.objects.all().order_by('name')

        if request.GET.get('search_name'):
            search_schools = models.School.objects.filter(name__icontains=request.GET.get('search_name'))
        elif request.GET.get('search_id'):
            search_schools = models.School.objects.filter(id=request.GET.get('search_id'))
        else:
            search_schools = None

        return render(request, 'school/secondary.html', {
            'all_schools':all_schools,
            'search_schools':search_schools,
        })


class SecondaryCreateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        all_schools = models.School.objects.all().order_by('name')
        provider_branches = bge_models.BgeBranch.objects.all().order_by('name')
        admission_coordi = user_models.BgeBranchCoordinator.objects.filter(position='admission_coordi')
        school_coordi = user_models.BgeBranchCoordinator.objects.filter(position='school_coordi')

        return render(request, 'school/create.html', {
            'all_schools':all_schools,
            'provider_branches':provider_branches,
            'admission_coordi':admission_coordi,
            'school_coordi':school_coordi,
        })

    def post(self, request):

        data = request.POST

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
            toefl_requirement = int(data.get('toefl_requirement')) if data.get('toefl_requirement') else None,
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


class SecondaryUpdateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, school_id=None):

        if not school_id:
            return HttpResponse(status=400)

        try:
            found_school = models.School.objects.get(pk=school_id)
        except models.School.DoesNotExist:
            return HttpResponse(status=400)

        all_schools = models.School.objects.all().order_by('name')
        provider_branches = bge_models.BgeBranch.objects.all().order_by('name')
        admission_coordi = user_models.BgeBranchCoordinator.objects.filter(position='admission_coordi')
        school_coordi = user_models.BgeBranchCoordinator.objects.filter(position='school_coordi')
        current_student_reviews = student_models.CurrentStudentReview.objects.filter(school=found_school).order_by('-created_at')
        graduate_profiles = student_models.GraduateStudentReview.objects.filter(school=found_school).order_by('-created_at')
        school_types = models.SchoolTypes.objects.filter(school=found_school)

        school_type_list = []
        for school_type in school_types:
            school_type_list.append(school_type.type)

        return render(request, 'school/update.html', {
            'found_school':found_school,
            'all_schools':all_schools,
            'provider_branches':provider_branches,
            'admission_coordi':admission_coordi,
            'school_coordi':school_coordi,
            'current_student_reviews':current_student_reviews,
            'graduate_profiles':graduate_profiles,
            'school_type_list':school_type_list,
        })

    def post(self, request, school_id=None):

        if not school_id:
            return HttpResponse(status=400)

        try:
            found_school = models.School.objects.get(pk=school_id)
        except models.School.DoesNotExist:
            return HttpResponse(status=400)

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

        found_school.name = data.get('name')
        found_school.image = uploaded_image if uploaded_image else None
        found_school.partnership = int(data.get('partnership')) if data.get('partnership') else None
        found_school.provider = data.get('provider')
        found_school.provider_branch = found_branch
        found_school.admission_coordi = found_admission_coordi
        found_school.school_coordi = found_school_coordi
        found_school.term = data.get('term')
        found_school.transfer = True if data.get('transfer') else False
        found_school.country = data.get('country')
        found_school.address = data.get('address')
        found_school.area_description = data.get('area_description')
        found_school.phone = data.get('phone')
        found_school.web_url = data.get('web_url')
        found_school.founded = data.get('founded')
        found_school.religion = data.get('religion')
        found_school.number_students = int(data.get('number_students')) if data.get('number_students') else None
        found_school.save()

        try:
            found_secodary = models.Secondary.objects.get(school=found_school)
        except models.Secondary.DoesNotExist:
            return HttpResponse(status=400)

        found_secodary.grade_start = int(data.get('grade_start')) if data.get('grade_start') else None
        found_secodary.grade_end = int(data.get('grade_end')) if data.get('grade_end') else None
        found_secodary.accept_12_grade = True if data.get('accept_12_grade') else False
        found_secodary.application_fee = int(data.get('application_fee')) if data.get('application_fee') else None
        found_secodary.program_fee = int(data.get('program_fee')) if data.get('program_fee') else None
        found_secodary.admission_requirements = data.get('admission_requirements')
        found_secodary.toefl_requirement = int(data.get('toefl_requirement')) if data.get('toefl_requirement') else None
        found_secodary.admission_documents = data.get('admission_documents')
        found_secodary.selling_point = data.get('selling_point')
        found_secodary.state = data.get('state')
        found_secodary.student_body = data.get('student_body')
        found_secodary.international_students = int(data.get('international_students')) if data.get('international_students') else None
        found_secodary.esl = True if data.get('esl') else False
        found_secodary.student_teach_ratio = data.get('student_teach_ratio')
        found_secodary.class_size = data.get('class_size')
        found_secodary.uniform = True if data.get('uniform') else False
        found_secodary.college_acceptance_rate = data.get('college_acceptance_rate')
        found_secodary.avg_sat = data.get('avg_sat')
        found_secodary.number_honor_courses = data.get('number_honor_courses')
        found_secodary.list_honor_courses = data.get('list_honor_courses')
        found_secodary.number_ap_courses = data.get('number_ap_courses')
        found_secodary.list_ap_courses = data.get('list_ap_courses')
        found_secodary.number_clubs = data.get('number_clubs')
        found_secodary.number_sports = data.get('number_sports')
        found_secodary.facilities = data.get('facilities')
        found_secodary.save()

        if data.get('school_type'):

            for school_type in data.getlist('school_type'):
                try:
                    found_school_type = models.SchoolTypes.filter(school=found_school, type=school_type)
                    continue
                except models.SchoolTypes.DoesNotExist:
                    school_types = models.SchoolTypes(
                        school = found_school,
                        type = school_type,
                    )
                    school_types.save()


        if request.FILES.get('photo'):

            if models.SchoolPhotos.objects.filter(school=found_school):
                found_photos = models.SchoolPhotos.objects.filter(school=found_school)
                found_photos.delete()

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


@login_required(login_url='/accounts/login/')
def current_review_create(request):

    if request.method == 'POST':

        data = request.POST

        if data.get('school_id'):
            try:
                found_school = models.School.objects.get(pk=int(data.get('school_id')))
            except models.School.DoesNotExist:
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=400)

        if data.get('student_id'):

            try:
                found_student = student_models.Student.objects.get(pk=int(data.get('student_id')))
            except student_models.Student.DoesNotExist:
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=400)

        if data.get('review_id'):

            try:
                found_review = student_models.CurrentStudentReview.objects.get(pk=int(data.get('review_id')))
            except student_models.CurrentStudentReview.DoesNotExist:
                return HttpResponse(status=400)

            found_review.student = found_student
            found_review.grade = data.get('grade')
            found_review.homecity = data.get('homecity')
            found_review.comment = data.get('comment')
            found_review.save()

        else:
            review = student_models.CurrentStudentReview(
                school=found_school,
                student=found_student,
                grade=data.get('grade'),
                homecity=data.get('homecity'),
                comment=data.get('comment'),
            )
            review.save()

    else:
        return HttpResponse(status=400)

    return HttpResponseRedirect(request.path_info)


@login_required(login_url='/accounts/login/')
def graduate_profile_create(request):

    if request.method == 'POST':

        data = request.POST

        if data.get('school_id'):
            try:
                found_school = models.School.objects.get(pk=int(data.get('school_id')))
            except models.School.DoesNotExist:
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=400)

        if data.get('student_id'):

            try:
                found_student = student_models.Student.objects.get(pk=int(data.get('student_id')))
            except student_models.Student.DoesNotExist:
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=400)

        if data.get('profile_id'):

            try:
                found_profile = student_models.GraduateStudentReview.objects.get(pk=int(data.get('profile_id')))
            except student_models.GraduateStudentReview.DoesNotExist:
                return HttpResponse(status=400)

            found_profile.student = found_student
            found_profile.attended = data.get('attended')
            found_profile.init_eng = data.get('init_eng')
            found_profile.gpa_china = data.get('gpa_china')
            found_profile.toefl = data.get('toefl')
            found_profile.gpa = data.get('gpa')
            found_profile.sat_act = data.get('sat_act')
            found_profile.activities = data.get('activities')
            found_profile.college = data.get('college')
            found_profile.major = data.get('major')
            found_profile.save()

        else:
            profile = student_models.GraduateStudentReview(
                school=found_school,
                student = found_student,
                attended = data.get('attended'),
                init_eng = data.get('init_eng'),
                gpa_china = data.get('gpa_china'),
                toefl = data.get('toefl'),
                gpa = data.get('gpa'),
                sat_act = data.get('sat_act'),
                activities = data.get('activities'),
                college = data.get('college'),
                major = data.get('major'),
            )
            profile.save()

    else:
        return HttpResponse(status=400)

    return HttpResponseRedirect(request.path_info)


@login_required(login_url='/accounts/login/')
def current_review_delete(request, review_id=None):

    if review_id:

        try:
            found_review = student_models.CurrentStudentReview.objects.get(pk=review_id)
        except student_models.CurrentStudentReview.DoesNotExist:
            return HttpResponse(status=400)

        found_review.delete()

        return HttpResponseRedirect(request.path_info)

    else:
        return HttpResponse(status=400)

@login_required(login_url='/accounts/login/')
def graduate_profile_delete(request, profile_id=None):

    if profile_id:
        try:
            found_profile = student_models.GraduateStudentReview.objects.get(pk=profile_id)
        except student_models.GraduateStudentReview.DoesNotExist:
            return HttpResponse(status=400)

        found_profile.delete()

        return HttpResponseRedirect(request.path_info)
    else:
        return HttpResponse(status=400)


class SecondaryReviewView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, secondary_id=None):


        return render(request, 'school/review.html', {})

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


class SecondaryEstimateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, secondary_id=None):


        return render(request, 'school/estimate.html', {})


class SecondaryPhotoView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, secondary_id=None):


        return render(request, 'school/photo.html', {})

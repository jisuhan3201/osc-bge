from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core import serializers
from . import models, forms
from osc_bge.users import models as user_models
from osc_bge.bge import models as bge_models
from osc_bge.student import models as student_models
from osc_bge.school import models as school_models
from osc_bge.form import models as form_models
from osc_bge.utils import render_to_pdf
import json

class SecondaryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def search(self):

        if self.request.GET.get('form_type') == 'secondary_form':

            queryset = models.Secondary.objects.all()

            school_type = self.request.GET.getlist('school_type', None)
            if school_type:
                queryset = queryset.filter(school__school_type__type__in=school_type)

            student_body = self.request.GET.getlist('student_body', None)
            if student_body:
                queryset = queryset.filter(student_body__in=student_body)

            grade = self.request.GET.getlist('grade', None)
            if grade:
                if len(grade) != 1:
                    queryset = queryset.filter(Q(grade_start__lte=grade[0]) | Q(grade_end__gte=grade[-1]))
                    to_schools = models.School.objects.filter(tb_of_og__grade__in=grade, tb_of_og__quantity__gt=0).distinct()
                    queryset = queryset.filter(school__in=to_schools)
                else:
                    queryset = queryset.filter(grade_start__lte=grade[0], grade_end__gte=grade[0])
                    to_schools = models.School.objects.filter(tb_of_og__grade=grade[0], tb_of_og__quantity__gt=0).distinct()
                    queryset = queryset.filter(school__in=to_schools)

            term = self.request.GET.getlist('term', None)
            if term:
                queryset = queryset.filter(school__term__in=term).distinct()
                to_schools = models.School.objects.filter(tb_of_og__term__in=term, tb_of_og__quantity__gt=0).distinct()
                queryset = queryset.filter(school__in=to_schools)

            toefl_requirement = self.request.GET.get('toefl_requirement', None)
            if toefl_requirement:
                if toefl_requirement == '100':
                    queryset = queryset.filter(toefl_requirement__gte=int(toefl_requirement), toefl_requirement__isnull=False)
                elif toefl_requirement == '0':
                    queryset = queryset.filter(toefl_requirement__isnull=True)
                else:
                    queryset =queryset.filter(toefl_requirement__lte=int(toefl_requirement), toefl_requirement__isnull=False)

            state = self.request.GET.getlist('state', None)
            if state:
                queryset = queryset.filter(state__in=state)


            transfer = self.request.GET.get('transfer', None)
            if transfer:
                queryset = queryset.filter(school__transfer=True)

            number_students = self.request.GET.getlist('number_students', None)
            if number_students:

                if not 's' in number_students:
                    queryset = queryset.exclude(school__number_students__lte=299).exclude(school__number_students__isnull=True)
                if not 'm' in number_students:
                    queryset = queryset.exclude(school__number_students__gte=300, school__number_students__lte=699).exclude(school__number_students__isnull=True)
                if not 'l' in number_students:
                    queryset = queryset.exclude(school__number_students__gte=700).exclude(school__number_students__isnull=True)

            program_fee = self.request.GET.get('program_fee', None)
            if program_fee:

                if program_fee == 'xs':
                    queryset = queryset.filter(program_fee__lte=35000)
                elif program_fee == 's':
                    queryset = queryset.filter(program_fee__lte=45000)
                elif program_fee == 'm':
                    queryset = queryset.filter(program_fee__lte=60000)
                elif program_fee == 'l':
                    queryset = queryset.filter(program_fee__gt=60000)
                else:
                    pass

        elif self.request.GET.get('form_type') == 'name_form':

            queryset = models.Secondary.objects.all()

            school_name = self.request.GET.get('school_name')
            if school_name:
                queryset = queryset.filter(school__name__icontains=school_name)

            school_id = self.request.GET.get('school_id')
            if school_id:
                queryset = models.Secondary.objects.filter(id=int(school_id))

        else:
            queryset = None

        return queryset

    def get(self, request):
        return HttpResponse(status=500)
        if request.user.type == 'bge_branch_admin':

            try:
                bge_branch_admin = user_models.BgeBranchAdminUser.objects.get(user=request.user)
                found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
            except:
                found_branch=None

            if not found_branch:
                try:
                    bge_branch_admin = user_models.BgeBranchCoordinator.objects.get(user=request.user)
                    found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
                except:
                    return HttpResponse('Not Branch Admin or Branch coordi', status=400)

            all_schools = models.Secondary.objects.filter(school__provider_branch=found_branch).order_by('school__name')

            if request.GET.get('search_name'):
                search_schools = models.Secondary.objects.filter(school__name__icontains=request.GET.get('search_name'), school__provider_branch=found_branch).order_by('school__name')
            elif request.GET.get('search_id'):
                search_schools = models.Secondary.objects.filter(school__id=request.GET.get('search_id'))
            else:
                search_schools = None

            if search_schools:
                for secondary in search_schools:
                    try:
                        last_log = models.SchoolCommunicationLog.objects.filter(school=secondary.school).latest('created_at')
                        secondary.last_log = last_log
                    except models.SchoolCommunicationLog.DoesNotExist:
                        secondary.last_log = None

            return render(request, 'school/secondary.html', {
                'all_schools':all_schools,
                'search_schools':search_schools,
            })

        else:
            secondaries = models.Secondary.objects.all().order_by("school__name", "school__partnership")
            search_schools = self.search()

            return render(request, 'school/secondary2.html',
                {
                    "secondaries":secondaries,
                    'search_schools':search_schools,
                }
            )


class CollegeView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def search(self):

        if self.request.GET.get('form_type') == 'college_form':

            queryset = models.College.objects.all().order_by('ranking')

            school_type = self.request.GET.getlist('school_type', None)
            if school_type:
                queryset = queryset.filter(school__school_type__type__in=school_type)

            toefl_requirement = self.request.GET.get('toefl_requirement', None)
            if toefl_requirement:
                if toefl_requirement == '100':
                    queryset = queryset.filter(toefl_requirement__gte=int(toefl_requirement), toefl_requirement__isnull=False)
                else:
                    queryset =queryset.filter(toefl_requirement__lte=int(toefl_requirement), toefl_requirement__isnull=False)

            state = self.request.GET.getlist('state', None)
            if state:
                queryset = queryset.filter(state__in=state)

            partition = self.request.GET.getlist('partition', None)
            if partition:
                queryset = queryset.filter(college_type__in=partition)

        elif self.request.GET.get('form_type') == 'name_form':

            queryset = models.College.objects.all()

            school_name = self.request.GET.get('school_name')
            if school_name:
                queryset = queryset.filter(school__name__icontains=school_name)

            school_id = self.request.GET.get('school_id')
            if school_id:
                queryset = models.College.objects.filter(id=int(school_id))

        else:
            queryset = None

        return queryset

    def get(self, request):
        return HttpResponse(status=500)
        all_schools = models.College.objects.all().order_by('ranking')
        first_schools = models.College.objects.filter(ranking__lte=50).order_by("ranking")
        second_schools = models.College.objects.filter(ranking__range=(51, 101)).order_by("ranking")
        third_schools = models.College.objects.filter(ranking__range=(101, 151)).order_by("ranking")
        fourth_schools = models.College.objects.filter(ranking__range=(151, 201)).order_by("ranking")
        search_schools = self.search()

        return render(request, 'school/colleges.html',
            {
                "first_schools":first_schools,
                "second_schools":second_schools,
                "third_schools":third_schools,
                "fourth_schools":fourth_schools,
                'search_schools':search_schools,
                'all_schools':all_schools
            }
        )


class SecondaryCreateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        return HttpResponse(status=500)
        secondaries = models.Secondary.objects.all()
        provider_branches = bge_models.BgeBranch.objects.all().order_by('name')
        admission_coordi = user_models.BgeBranchCoordinator.objects.filter(position='admission_coordi')
        school_coordi = user_models.BgeBranchCoordinator.objects.filter(position='school_coordi')
        to_range = range(7, 13)

        return render(request, 'school/create.html', {
            'secondaries':secondaries,
            'provider_branches':provider_branches,
            'admission_coordi':admission_coordi,
            'school_coordi':school_coordi,
            'to_range': to_range,
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
                found_school_coordi = user_models.BgeBranchCoordinator.objects.get(pk=int(data.get('school_coordi')))
            except user_models.BgeBranchCoordinator.DoesNotExist:
                return HttpResponse(status=400)
        else:
            found_school_coordi = None

        school = models.School(
            name = data.get('name'),
            type = 'secondary',
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

        image_form = forms.SchoolImageForm(request.POST,request.FILES)
        if image_form.is_valid():
            school.image = image_form.cleaned_data['image']
            school.save()

        if request.FILES.getlist('photo'):
            photo_form = forms.SchoolPhotoForm(request.POST, request.FILES)
            if photo_form.is_valid():
                for photo in request.FILES.getlist('photo'):

                    school_photo = models.SchoolPhotos()
                    school_photo.school = found_school
                    school_photo.photo = photo
                    school_photo.save()

        for num in range(7 ,13):


            found_school_fall_to = models.SchoolTotalQuantity(
                school=school,
                term='fall',
                grade=num,
                quantity=int(data.get('to_value_fall_'+str(num))) if data.get('to_value_fall_'+str(num)) else 0
            )
            found_school_fall_to.save()

            found_school_spring_to = models.SchoolTotalQuantity(
                school=school,
                term='spring',
                grade=num,
                quantity=int(data.get('to_value_spring_'+str(num))) if data.get('to_value_spring_'+str(num)) else 0
            )
            found_school_spring_to.save()

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
            list_clubs = data.get('list_clubs'),
            number_sports = data.get('number_sports'),
            list_sports = data.get('list_sports'),
            facilities = data.get('facilities'),
            general_impression = data.get('general_impression'),
            strong_advantages = data.get('strong_advantages'),
            extra_curricular = data.get('extra_curricular'),
            college_acceptance_list = data.get("college_acceptance_list"),
            fee_memo=data.get('fee_memo'),
        )
        secondary.save()

        if data.get('school_type'):

            for school_type in data.getlist('school_type'):
                school_types = models.SchoolTypes(
                    school = school,
                    type = school_type,
                )
                school_types.save()


        return redirect('/school/secondary')


class SecondaryUpdateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, school_id=None):
        return HttpResponse(status=500)
        if not school_id:
            return HttpResponse(status=400)

        try:
            found_school = models.School.objects.get(pk=school_id)
        except models.School.DoesNotExist:
            return HttpResponse(status=400)

        secondaries = models.Secondary.objects.all()
        provider_branches = bge_models.BgeBranch.objects.all().order_by('name')
        admission_coordi = user_models.BgeBranchCoordinator.objects.filter(position='admission_coordi')
        school_coordi = user_models.BgeBranchCoordinator.objects.filter(position='school_coordi')
        current_student_reviews = student_models.CurrentStudentReview.objects.filter(school=found_school).order_by('-created_at')
        graduate_profiles = student_models.GraduateStudentReview.objects.filter(school=found_school).order_by('-created_at')
        school_types = models.SchoolTypes.objects.filter(school=found_school)

        school_type_list = []
        for school_type in school_types:
            school_type_list.append(school_type.type)

        to_range = range(7, 13)

        try:
            found_school_to = models.SchoolTotalQuantity.objects.filter(school=found_school)
        except models.SchoolTotalQuantity.DoesNotExist:
            found_school_to = None

        return render(request, 'school/update.html', {
            'found_school':found_school,
            'secondaries':secondaries,
            'provider_branches':provider_branches,
            'admission_coordi':admission_coordi,
            'school_coordi':school_coordi,
            'current_student_reviews':current_student_reviews,
            'graduate_profiles':graduate_profiles,
            'school_type_list':school_type_list,
            'current_student_reviews':current_student_reviews,
            "graduate_profiles":graduate_profiles,
            'to_range':to_range,
            "found_school_to":found_school_to,
        })

    def post(self, request, school_id=None):

        data = request.POST

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
                found_school_coordi = user_models.BgeBranchCoordinator.objects.get(pk=int(data.get('school_coordi')))
            except user_models.BgeBranchCoordinator.DoesNotExist:
                return HttpResponse(status=400)
        else:
            found_school_coordi = None


        found_school.name = data.get('name')
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

        if request.FILES.get('image'):
            image_form = forms.SchoolImageForm(request.POST,request.FILES)
            if image_form.is_valid():
                found_school.image = image_form.cleaned_data['image']
                found_school.save()

        if request.FILES.getlist('photo'):
            photo_form = forms.SchoolPhotoForm(request.POST, request.FILES)
            if photo_form.is_valid():
                for photo in request.FILES.getlist('photo'):

                    school_photo = models.SchoolPhotos()
                    school_photo.school = found_school
                    school_photo.photo = photo
                    school_photo.save()

        if data.getlist('delete_photo'):
            for photo_id in data.getlist('delete_photo'):
                found_school_photo = models.SchoolPhotos.objects.get(id=int(photo_id))
                found_school_photo.delete()

        for num in range(7 ,13):

            if data.get('to_value_fall_'+ str(num)):

                try:
                    found_school_fall_to = models.SchoolTotalQuantity.objects.get(school=found_school, term='fall', grade=num)
                    found_school_fall_to.quantity = int(data.get('to_value_fall_'+str(num)))
                    found_school_fall_to.save()
                except models.SchoolTotalQuantity.DoesNotExist:
                    found_school_fall_to = models.SchoolTotalQuantity(
                        school=found_school,
                        term='fall',
                        grade=int(data.get('to_grade_fall_'+str(num))) if data.get('to_grade_fall_'+str(num)) else None,
                        quantity=int(data.get('to_value_fall_'+str(num))) if data.get('to_value_fall_'+str(num)) else None
                    )
                    found_school_fall_to.save()

            if data.get('to_value_spring_'+ str(num)):

                try:
                    found_school_spring_to = models.SchoolTotalQuantity.objects.get(school=found_school, term='spring', grade=num)
                    found_school_spring_to.quantity = int(data.get('to_value_spring_'+str(num)))
                    found_school_spring_to.save()
                except models.SchoolTotalQuantity.DoesNotExist:
                    found_school_spring_to = models.SchoolTotalQuantity(
                        school=found_school,
                        term='spring',
                        grade=int(data.get('to_grade_spring_'+str(num))) if data.get('to_grade_spring_'+str(num)) else None,
                        quantity=int(data.get('to_value_spring_'+str(num))) if data.get('to_value_spring_'+str(num)) else None
                    )
                    found_school_spring_to.save()

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
        found_secodary.list_clubs = data.get('list_clubs')
        found_secodary.number_sports = data.get('number_sports')
        found_secodary.list_sports = data.get('list_sports')
        found_secodary.facilities = data.get('facilities')
        found_secodary.general_impression = data.get('general_impression')
        found_secodary.strong_advantages = data.get('strong_advantages')
        found_secodary.extra_curricular = data.get('extra_curricular')
        found_secodary.college_acceptance_list = data.get("college_acceptance_list")
        found_secodary.fee_memo = data.get('fee_memo')

        found_secodary.save()

        if data.get('school_type'):

            if models.SchoolTypes.objects.filter(school=found_school):
                found_types = models.SchoolTypes.objects.filter(school=found_school)
                found_types.delete()

            for school_type in data.getlist('school_type'):

                school_types = models.SchoolTypes(
                    school = found_school,
                    type = school_type,
                )
                school_types.save()

        return redirect(request.path_info)


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

        if data.get('review_id'):

            try:
                found_review = student_models.CurrentStudentReview.objects.get(pk=int(data.get('review_id')))
            except student_models.CurrentStudentReview.DoesNotExist:
                return HttpResponse(status=400)

            found_review.student = data.get('student')
            found_review.grade = data.get('grade')
            found_review.homecity = data.get('homecity')
            found_review.comment = data.get('comment')
            found_review.save()

        else:
            review = student_models.CurrentStudentReview(
                school=found_school,
                student=data.get('student'),
                grade=data.get('grade'),
                homecity=data.get('homecity'),
                comment=data.get('comment'),
            )
            review.save()

    else:
        return HttpResponse(status=400)

    return HttpResponseRedirect("/school/secondary/update/"+data.get('school_id'))


@login_required(login_url='/accounts/login')
def current_review_get(request, review_id=None):

    if review_id:

        try:
            found_review = student_models.CurrentStudentReview.objects.filter(pk=review_id)
        except student_models.CurrentStudentReview.DoesNotExist:
            return HttpResponse("Review ID does not exist", status=400)

        data = serializers.serialize("json", found_review)

        return HttpResponse(data, content_type="application/json")

    else:
        return HttpResponse("Review ID IS NULL", statue=400)


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

        if data.get('profile_id'):

            try:
                found_profile = student_models.GraduateStudentReview.objects.get(pk=int(data.get('profile_id')))
            except student_models.GraduateStudentReview.DoesNotExist:
                return HttpResponse(status=400)

            found_profile.student = data.get('student')
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
                student = data.get('student'),
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

    return HttpResponseRedirect("/school/secondary/update/"+data.get('school_id'))


@login_required(login_url='/accounts/login')
def graduate_profile_get(request, profile_id=None):

    if profile_id:

        try:
            found_profile = student_models.GraduateStudentReview.objects.filter(pk=profile_id)
        except student_models.GraduateStudentReview.DoesNotExist:
            return HttpResponse("Profile ID does not exist", status=400)

        data = serializers.serialize("json", found_profile)
        return HttpResponse(data, content_type="application/json")

    else:
        return HttpResponse("Profile ID IS NULL", statue=400)


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


class SecondaryLogView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, school_id=None):
        return HttpResponse(status=500)
        if school_id:

            try:
                bge_branch_admin = user_models.BgeBranchAdminUser.objects.get(user=request.user)
                found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
            except:
                found_branch=None

            if not found_branch:
                try:
                    bge_branch_admin = user_models.BgeBranchCoordinator.objects.get(user=request.user)
                    found_branch = bge_models.BgeBranch.objects.get(id=bge_branch_admin.branch.id)
                except:
                    return HttpResponse('Not Branch Admin or Branch coordi', status=400)

            all_schools = school_models.Secondary.objects.filter(school__provider_branch=found_branch)

            try:
                found_school = school_models.School.objects.get(pk=school_id)
            except school_models.School.DoesNotExist:
                return HttpResponse("Wrong school id", status=400)

            found_logs = models.SchoolCommunicationLog.objects.filter(school=found_school).order_by("-created_at")

        else:
            return HttpResponse('No school id', status=400)

        return render(request, 'school/school_log.html', {
            "all_schools":all_schools,
            "found_school":found_school,
            "found_logs":found_logs,
        })


    def post(self, request, school_id=None):

        data = request.POST

        if school_id:

            if data.get('log_id'):
                found_log = models.SchoolCommunicationLog.objects.get(id=int(data.get('log_id')))
                found_log.delete()
                return HttpResponseRedirect(request.path_info)

            try:
                found_school = school_models.School.objects.get(pk=school_id)
            except school_models.School.DoesNotExist:
                return HttpResponse("Wrong school id", status=400)

            log = models.SchoolCommunicationLog(
                school=found_school,
                writer=request.user,
                comment=data.get('comment'),
            )
            log.save()

            log_form = forms.SchoolLogForm(request.POST,request.FILES)
            if log_form.is_valid():
                log.file = log_form.cleaned_data['file']
                log.save()

        else:
            return HttpResponse(status=400)

        return HttpResponseRedirect(request.path_info)


class CollegeSchoolView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, school_id=None):
        return HttpResponse(status=500)
        if school_id:

            try:
                found_school = school_models.School.objects.get(pk=school_id)
            except school_models.School.DoesNotExist:
                return HttpResponse("Wrong school id", status=400)

        else:
            return HttpResponse('No school id', status=400)

        return render(request, 'agent_school/colleges.html', {'found_school':found_school})


class SecondarySummaryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get_counselor(self):

        user = self.request.user
        try:
            found_counselor = user_models.Counselor.objects.get(user=user)
        except user_models.Counselor.DoesNotExist:
            return HttpResponse(status=401)
        return found_counselor

    def get(self, request, school_id=None):
        return HttpResponse(status=500)
        found_counselor = self.get_counselor()

        if school_id:

            try:
                found_school = school_models.School.objects.get(pk=school_id)
            except school_models.School.DoesNotExist:
                return HttpResponse("Wrong school id", status=400)

            try:
                selling_point = form_models.CounselorSellingPoint.objects.get(
                    school=found_school, counselor=found_counselor)
            except:
                selling_point = None
        else:
            return HttpResponse("School id is null", statue=400)

        return render(request, 'school/summary.html', {
            'found_school':found_school,
            'selling_point':selling_point,
        })

    def post(self, request, school_id=None):

        data = request.POST
        found_counselor = self.get_counselor()

        if school_id:

            try:
                found_school = school_models.School.objects.get(pk=school_id)
            except school_models.School.DoesNotExist:
                return HttpResponse("Wrong school id", status=400)

            if data.get('counselling_point_id'):

                try:
                    found_counselling_point = form_models.CounselorSellingPoint.objects.get(id=int(data.get('counselling_point_id')))
                except form_models.CounselorSellingPoint.DoesNotExist:
                    return HttpResponse(status=400)

                found_counselling_point.location_ev=data.get('location_ev')
                found_counselling_point.location_cm=data.get('location_cm')
                found_counselling_point.admission_requirement_ev=data.get('admission_requirement_ev')
                found_counselling_point.admission_requirement_cm=data.get('admission_requirement_cm')
                found_counselling_point.student_number_ev=data.get('student_number_ev')
                found_counselling_point.student_number_cm=data.get('student_number_cm')
                found_counselling_point.intl_student_number_ev=data.get('intl_student_number_ev')
                found_counselling_point.intl_student_number_cm=data.get('intl_student_number_cm')
                found_counselling_point.esl_ev=data.get('esl_ev')
                found_counselling_point.esl_cm=data.get('esl_cm')
                found_counselling_point.student_teacher_ratio_ev=data.get('student_teacher_ratio_ev')
                found_counselling_point.student_teacher_ratio_cm=data.get('student_teacher_ratio_cm')
                found_counselling_point.application_fee_ev=data.get('application_fee_ev')
                found_counselling_point.application_fee_cm=data.get('application_fee_cm')
                found_counselling_point.program_fee_ev=data.get('program_fee_ev')
                found_counselling_point.program_fee_cm=data.get('program_fee_cm')
                found_counselling_point.ap_ev=data.get('ap_ev')
                found_counselling_point.ap_cm=data.get('ap_cm')
                found_counselling_point.honor_ev=data.get('honor_ev')
                found_counselling_point.honor_cm=data.get('honor_cm')
                found_counselling_point.clubs_ev=data.get('clubs_ev')
                found_counselling_point.clubs_cm=data.get('clubs_cm')
                found_counselling_point.sports_ev=data.get('sports_ev')
                found_counselling_point.sports_cm=data.get('sports_cm')
                found_counselling_point.save()

            else:
                found_counselling_point = form_models.CounselorSellingPoint(
                    school=found_school,
                    counselor=found_counselor,
                    location_ev=data.get('location_ev'),
                    location_cm=data.get('location_cm'),
                    admission_requirement_ev=data.get('admission_requirement_ev'),
                    admission_requirement_cm=data.get('admission_requirement_cm'),
                    student_number_ev=data.get('student_number_ev'),
                    student_number_cm=data.get('student_number_cm'),
                    intl_student_number_ev=data.get('intl_student_number_ev'),
                    intl_student_number_cm=data.get('intl_student_number_cm'),
                    esl_ev=data.get('esl_ev'),
                    esl_cm=data.get('esl_cm'),
                    student_teacher_ratio_ev=data.get('student_teacher_ratio_ev'),
                    student_teacher_ratio_cm=data.get('student_teacher_ratio_cm'),
                    application_fee_ev=data.get('application_fee_ev'),
                    application_fee_cm=data.get('application_fee_cm'),
                    program_fee_ev=data.get('program_fee_ev'),
                    program_fee_cm=data.get('program_fee_cm'),
                    ap_ev=data.get('ap_ev'),
                    ap_cm=data.get('ap_cm'),
                    honor_ev=data.get('honor_ev'),
                    honor_cm=data.get('honor_cm'),
                    clubs_ev=data.get('clubs_ev'),
                    clubs_cm=data.get('clubs_cm'),
                    sports_ev=data.get('sports_ev'),
                    sports_cm=data.get('sports_cm'),
                )
                found_counselling_point.save()


        else:
            return HttpResponse('No school id', status=400)

        return HttpResponseRedirect(request.path_info)

class SecondaryDetailView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get_counselor(self):

        user = self.request.user
        try:
            found_counselor = user_models.Counselor.objects.get(user=user)
        except user_models.Counselor.DoesNotExist:
            return HttpResponse(status=401)
        return found_counselor

    def get(self, request, school_id=None):
        return HttpResponse(status=500)
        found_counselor = self.get_counselor()

        if school_id:

            try:
                found_school = school_models.School.objects.get(pk=school_id)
            except school_models.School.DoesNotExist:
                return HttpResponse("Wrong school id", status=400)

            school_types = school_models.SchoolTypes.objects.filter(school=found_school)
        else:
            return HttpResponse("School id is null", statue=400)

        return render(request, 'school/detailed_info.html', {
            'found_school':found_school,
            'school_types':school_types,
        })


class SecondaryServiceView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, school_id=None):
        return HttpResponse(status=500)
        if school_id:

            try:
                found_school = school_models.School.objects.get(pk=school_id)
            except school_models.School.DoesNotExist:
                return HttpResponse("Wrong school id", status=400)

        else:
            return HttpResponse("School id is null", statue=400)

        all_videos = bge_models.BgeVideo.objects.all()

        return render(request, 'school/service.html', {
            'found_school':found_school,
            'all_videos':all_videos,
        })


class SecondaryReviewView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, school_id=None):
        return HttpResponse(status=500)
        if school_id:

            try:
                found_school = school_models.School.objects.get(pk=school_id)
            except school_models.School.DoesNotExist:
                return HttpResponse("Wrong school id", status=400)

            current_student_reviews = student_models.CurrentStudentReview.objects.filter(
                school=found_school).order_by("-created_at")
            graduate_student_reviews = student_models.GraduateStudentReview.objects.filter(
                school=found_school).order_by("-created_at")

        else:
            return HttpResponse("School id is null", statue=400)

        return render(request, 'school/review.html', {
            'found_school':found_school,
            'current_student_reviews':current_student_reviews,
            'graduate_student_reviews':graduate_student_reviews,
        })


class SecondaryEstimateView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, school_id=None):
        return HttpResponse(status=500)
        if school_id:

            try:
                found_school = school_models.School.objects.get(pk=school_id)
            except school_models.School.DoesNotExist:
                return HttpResponse("Wrong school id", status=400)

        else:
            return HttpResponse("School id is null", statue=400)

        return render(request, 'school/estimate.html', {
            'found_school':found_school,
        })


class SecondaryPhotoView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, school_id=None):
        return HttpResponse(status=500)
        if school_id:

            try:
                found_school = school_models.School.objects.get(pk=school_id)
            except school_models.School.DoesNotExist:
                return HttpResponse("Wrong school id", status=400)

        else:
            return HttpResponse("School id is null", statue=400)

        return render(request, 'school/photo.html', {
            'found_school':found_school,
        })


class SecondaryDetailPdfView(View):

    def get(self, request, school_id=None):
        return HttpResponse(status=500)
        if school_id:

            try:
                found_school = school_models.School.objects.get(pk=school_id)
            except school_models.School.DoesNotExist:
                return HttpResponse("Wrong school id", status=400)

            school_types = school_models.SchoolTypes.objects.filter(school=found_school)
        else:
            return HttpResponse("School id is null", statue=400)

        data = {
             'found_school':found_school,
             'school_types':school_types,
        }
        pdf = render_to_pdf('school/detailed_info.html', data)


        return HttpResponse(pdf, content_type='application/pdf')

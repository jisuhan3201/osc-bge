from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from django.db.models import Q
from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . import models, forms
from osc_bge.users import models as user_models
from osc_bge.form import models as form_models
from osc_bge.form import forms as form_forms
from osc_bge.student import models as student_models
from osc_bge.student import forms as student_forms
from osc_bge.school import models as school_models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
from decimal import Decimal
from datetime import datetime, date


class StatisticsView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        user = request.user
        agency = None
        agency_head = None
        if user.type == "counselor":
            return HttpResponse(status=401)

        elif user.type == 'agency_branch_admin':
            try:
                agency_branch_admin = user_models.AgencyAdminUser.objects.get(user=user)
                agency = agency_branch_admin.agency
            except user_models.AgencyAdminUser.DoesNotExist:
                return HttpResponse(status=401)
        elif user.type == 'agency_admin':
            try:
                agency_admin = user_models.AgencyHeadAdminUser.objects.get(user=user)
                agency_head = agency_admin.agency_head
            except user_models.AgencyHeadAdminUser.DoesNotExist:
                return HttpResponse(status=401)


        # 1st section statistics

        total_counsel = 0
        total_registered = 0
        total_secondary = 0
        total_college = 0
        total_camp = 0
        total_us_count = 0
        total_ca_count = 0
        total_uk_count = 0
        total_au_count = 0
        total_nz_count = 0

        # 2nd Section statistics
        monthly_data = {}
        past_date_range = []
        past_date_first = []

        if self.request.GET.get('past_months'):

            today = date.today()
            past_months = int(self.request.GET.get('past_months'))

            for number in range(0, past_months+1):

                sd = today - relativedelta(months=number)
                ed = today - relativedelta(months=number-1)

                past_start_date = date(sd.year, sd.month, 1)
                past_end_date = date(ed.year, ed.month, 1) - relativedelta(days=1)
                past_date_range.append([past_start_date, past_end_date])
                past_date_first.append(past_start_date)

        if agency:
            counselors = user_models.Counselor.objects.filter(agency=agency)
        elif agency_head:
            counselors = user_models.Counselor.objects.filter(agency__head=agency_head)
        else:
            counselors.Counselor.objects.all()

        for counselor in counselors:

            # For 1st Section statistics
            query_start_date = self.request.GET.get('start_date', None)
            query_end_date = self.request.GET.get('end_date', None)
            if query_start_date or query_end_date:
                found_counsels = form_models.Counsel.objects.filter(counselor=counselor).filter(
                    created_at__range=(query_start_date, query_end_date))
                found_formalities = form_models.Formality.objects.filter(counsel__counselor=counselor).filter(
                    counsel__created_at__range=(query_start_date, query_end_date))
            else:
                found_counsels = form_models.Counsel.objects.filter(counselor=counselor)
                found_formalities = form_models.Formality.objects.filter(counsel__counselor=counselor)

            # For 2nd Section statistics
            if past_date_range:

                data_list = []

                for date_range in past_date_range:
                    data_dict = {}
                    date_first = date_range[0]
                    monthly_counsels = form_models.Counsel.objects.filter(counselor=counselor).filter(
                        created_at__range=(date_range[0], date_range[1]))
                    monthly_formality_count = form_models.Formality.objects.filter(counsel__counselor=counselor).filter(
                        counsel__created_at__range=(date_range[0], date_range[1])).count()
                    if request.GET.get('school_type'):
                        monthly_counsels = monthly_counsels.filter(program_interested=request.GET.get('school_type'))
                        monthly_formality_count = form_models.Formality.objects.filter(counsel__counselor=counselor).filter(
                        counsel__created_at__range=(date_range[0], date_range[1])).filter(
                        counsel__program_interested=request.GET.get('school_type')).count()
                    monthly_counsels_count = monthly_counsels.count()
                    try:
                        monthly_success_rate = int(monthly_formality_count * 100 / monthly_counsels_count)
                    except ZeroDivisionError:
                        monthly_success_rate = 0
                    data_dict.update({
                        'date_first':date_first,
                        'monthly_counsels_count':monthly_counsels_count,
                        'monthly_formality_count':monthly_formality_count,
                        'monthly_success_rate':monthly_success_rate,
                    })
                    data_list.append(data_dict)

                counselor_fullname = counselor.agency.name + " / " + counselor.user.first_name + " " + counselor.user.last_name
                monthly_data.update({counselor_fullname:data_list})

            counsel_count = found_counsels.count()
            total_counsel += counsel_count
            formality_count = found_formalities.count()
            total_registered += formality_count

            try:
                apply_percentage = formality_count * 100 / counsel_count
                apply_percentage = int(apply_percentage)
            except ZeroDivisionError:
                apply_percentage = 0

            secondary_count = 0
            college_count = 0
            camp_count = 0
            us_count = 0
            ca_count = 0
            uk_count = 0
            au_count = 0
            nz_count = 0

            for counsel in found_counsels:

                if counsel.program_interested == 'k12':
                    secondary_count += 1
                elif counsel.program_interested == 'college':
                    college_count += 1
                elif counsel.program_interested == 'camp':
                    camp_count += 1
                else:
                    continue

                if counsel.desire_country == 'us':
                    us_count += 1
                elif counsel.desire_country == 'ca':
                    ca_count += 1
                elif counsel.desire_country == 'uk':
                    uk_count += 1
                elif counsel.desire_country == 'au':
                    au_count += 1
                elif counsel.desire_country == 'nz':
                    nz_count += 1
                else:
                    continue

            counselor.counsel_count = counsel_count
            counselor.formality_count = formality_count
            counselor.apply_percentage = apply_percentage
            counselor.secondary = secondary_count
            counselor.college = college_count
            counselor.camp = camp_count
            counselor.us_count = us_count
            counselor.ca_count = ca_count
            counselor.uk_count = uk_count
            counselor.au_count = au_count
            counselor.nz_count = nz_count
            counselor.save()

            total_secondary += secondary_count
            total_college += college_count
            total_camp += camp_count
            total_us_count += us_count
            total_ca_count += ca_count
            total_uk_count += uk_count
            total_au_count += au_count
            total_nz_count += nz_count


        try:
            total_success_rate = int(total_registered * 100 / total_counsel)
        except ZeroDivisionError:
            total_success_rate = 0

        # Make range of months for templates
        template_date_range = []
        today = date.today()
        for number in range(0, 13):

            sd = today - relativedelta(months=number)
            ed = today - relativedelta(months=number-1)

            past_start_date = date(sd.year, sd.month, 1)
            past_end_date = date(ed.year, ed.month, 1) - relativedelta(days=1)
            template_date_range.append([past_start_date, past_end_date])


        return render(request, 'agent/statistics.html', {
            "counselors":counselors,
            'total_counsel':total_counsel,
            'total_registered':total_registered,
            'total_success_rate':total_success_rate,
            'total_secondary':total_secondary,
            'total_college':total_college,
            'total_camp':total_camp,
            'total_us_count':total_us_count,
            'total_ca_count':total_ca_count,
            'total_uk_count':total_uk_count,
            'total_au_count':total_au_count,
            'total_nz_count':total_nz_count,
            'monthly_data':monthly_data,
            'past_date_first':past_date_first,
            'template_date_range':template_date_range,
        })


class CounselView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def search(self):

        if self.request.GET.get('form_type') == 'secondary_form':

            queryset = school_models.Secondary.objects.all().order_by('school__partnership', 'school__name')

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
                    to_schools = school_models.School.objects.filter(tb_of_og__grade__in=grade, tb_of_og__quantity__gt=0).distinct()
                    queryset = queryset.filter(school__in=to_schools)
                else:
                    queryset = queryset.filter(grade_start__lte=grade[0], grade_end__gte=grade[0])
                    to_schools = school_models.School.objects.filter(tb_of_og__grade=grade[0], tb_of_og__quantity__gt=0).distinct()
                    queryset = queryset.filter(school__in=to_schools)

            term = self.request.GET.getlist('term', None)
            if term:
                queryset = queryset.filter(school__term__in=term).distinct()
                to_schools = school_models.School.objects.filter(tb_of_og__term__in=term, tb_of_og__quantity__gt=0).distinct()
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

        elif self.request.GET.get('form_type') == 'college_form':
            queryset = school_models.College.objects.all().order_by('ranking')

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

            queryset = school_models.Secondary.objects.all().order_by('school__partnership', 'school__name')

            school_name = self.request.GET.get('school_name')
            if school_name:
                queryset = queryset.filter(school__name__icontains=school_name)

            school_id = self.request.GET.get('school_id')
            if school_id:
                queryset = school_models.Secondary.objects.filter(id=int(school_id))

        elif self.request.GET.get('form_type') == 'college_name_form':

            queryset = school_models.College.objects.all()

            school_name = self.request.GET.get('school_name')
            if school_name:
                queryset = queryset.filter(school__name__icontains=school_name)

            school_id = self.request.GET.get('school_id')
            if school_id:
                queryset = school_models.College.objects.filter(id=int(school_id))

        else:
            queryset = None

        return queryset


    def get(self, request):

        secondaries = school_models.Secondary.objects.all().order_by('school__partnership', 'school__name')
        colleges = school_models.College.objects.all().order_by('ranking')
        search_schools = self.search()

        return render(request, 'agent/counsel.html',
            {
                "secondaries":secondaries,
                "colleges":colleges,
                'search_schools':search_schools,
            }
        )


class CustomerRegisterView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get_counselor(self):

        user = self.request.user
        try:
            found_counselor = user_models.Counselor.objects.get(user=user)
        except user_models.Counselor.DoesNotExist:
            return HttpResponse(status=401)
        return found_counselor

    def get(self, request, counsel_num=None):

        if counsel_num:

            try:
                found_counsel = form_models.Counsel.objects.get(pk=counsel_num)
            except form_models.Counsel.DoesNotExist:
                return HttpResponse(status=404)

            if request.user.type == 'counselor':
                found_counselor = self.get_counselor()

                if not found_counsel.counselor == found_counselor:
                    return HttpResponse(status=401)

            try:
                student_history = student_models.StudentHistory.objects.get(student=found_counsel.student)
            except:
                student_history = None
            return render(request, 'agent/register.html', {"counsel":found_counsel, "student_history": student_history})

        return render(request, 'agent/register.html', {})

    def post(self, request, counsel_num=None):

        data = request.POST
        if request.user.type == 'counselor':
            found_counselor = self.get_counselor()

        if counsel_num:
            try:
                found_counsel = form_models.Counsel.objects.get(pk=counsel_num)
            except form_models.Counsel.DoesNotExist:
                return HttpResponse(status=404)

            if request.user.type == 'counselor':
                if not found_counselor == found_counsel.counselor:
                    return HttpResponse(status=401)

            parent_info = None
            if (data.get('parentname') or data.get('parentcell') or
                    data.get('parentemail') or data.get('parentwechat')):

                try:
                    parent_info = found_counsel.student.parent_info
                    parent_info.name = data.get('parentname')
                    parent_info.phone = data.get('parentcell')
                    parent_info.email = data.get('parentemail')
                    parent_info.wechat = data.get('parentwechat')
                    parent_info.save()
                except:
                    parent_info = student_models.ParentInfo(
                        name=data.get('parentname'),
                        phone=data.get('parentcell'),
                        email=data.get('parentemail'),
                        wechat=data.get('parentwechat'),
                    )
                    parent_info.save()

            student = found_counsel.student
            if request.user.type == 'counselor':
                student.counselor=found_counselor
            student.parent_info = parent_info
            student.name = data.get('name')
            student.gender = data.get('gender')
            student.birthday = data.get('birth')
            student.email = data.get('email')
            student.skype = data.get("skype")
            student.nationality = data.get("nationality")
            student.wechat = data.get('wechat')
            student.phone = data.get('phone')
            student.save()

            image_form = student_forms.StudentImageForm(request.POST,request.FILES)
            if image_form.is_valid():
                student.image = image_form.cleaned_data['image']
                student.save()

            counsel = found_counsel
            counsel.student = student
            counsel.program_interested = data.get('program')
            counsel.expected_departure = data.get('departure')
            counsel.possibility = data.get('possibility')
            counsel.client_class = data.get('class')
            counsel.contact_first = data.get('contact1th')
            counsel.contact_second = data.get('contact2th')
            counsel.contact_third = data.get('contact3th')
            counsel.detail = data.get('detail')
            counsel.save()

            try:
                student_history = student_models.StudentHistory.objects.get(student=student)
                student_history.student = student
                student_history.current_grade = data.get('currentgrade')
                student_history.current_school=data.get('currentschool')
                student_history.apply_grade=data.get('gradeapply')
                student_history.eng_level=data.get('englevel')
                student_history.toefl=data.get('toefl')
                student_history.toefljr=data.get('toefljr')
                student_history.gpa=data.get('gpa')
                student_history.sat=data.get('sat')
                student_history.address=data.get('address')
                student_history.save()

            except student_models.StudentHistory.DoesNotExist:
                student_history = student_models.StudentHistory(
                    student=student,
                    current_grade=data.get('currentgrade'),
                    current_school=data.get('currentschool'),
                    apply_grade=data.get('gradeapply'),
                    eng_level=data.get('englevel'),
                    toefl=data.get('toefl'),
                    toefljr=data.get('toefljr'),
                    gpa=data.get('gpa'),
                    sat=data.get('sat'),
                    address=data.get('address'),
                )
                student_history.save()

        else:
            parent_info = False
            if (data.get('parentname') or data.get('parentcell') or
                    data.get('parentemail') or data.get('parentwechat')):

                parent_info = student_models.ParentInfo(
                    name=data.get('parentname'),
                    phone=data.get('parentcell'),
                    email=data.get('parentemail'),
                    wechat=data.get('parentwechat'),
                )
                parent_info.save()

            student = student_models.Student(
                counselor=found_counselor,
                parent_info=parent_info if parent_info else None,
                name=data.get('name'),
                gender=data.get('gender'),
                birthday=data.get('birth'),
                email=data.get('email'),
                skype=data.get('skype'),
                nationality=data.get('nationality'),
                wechat=data.get('wechat'),
                phone=data.get('phone'),
            )
            student.save()

            image_form = student_forms.StudentImageForm(request.POST,request.FILES)
            if image_form.is_valid():
                student.image = image_form.cleaned_data['image']
                student.save()

            counsel = form_models.Counsel(
                counselor=found_counselor,
                student=student,
                counseling_date=data.get('date'),
                desire_country=data.get('country'),
                program_interested=data.get('program'),
                expected_departure=data.get('departure'),
                possibility=data.get('possibility'),
                client_class=data.get('class'),
                contact_first=data.get('contact1th'),
                contact_second=data.get('contact2th'),
                contact_third=data.get('contact3th'),
                detail=data.get('detail'),
            )
            counsel.save()

            if (
                data.get('toefl') or data.get('toefljr') or data.get('gpa') or
                    data.get('sat') or data.get('englevel') or data.get('currentschool') or
                        data.get('currentgrade') or data.get('gradeapply') or data.get('address')):

                student_history = student_models.StudentHistory(
                    student=student,
                    current_grade=data.get('currentgrade'),
                    current_school=data.get('currentschool'),
                    apply_grade=data.get('gradeapply'),
                    eng_level=data.get('englevel'),
                    toefl=data.get('toefl'),
                    toefljr=data.get('toefljr'),
                    gpa=data.get('gpa'),
                    sat=data.get('sat'),
                    address=data.get('address'),
                )
                student_history.save()

        return HttpResponseRedirect(request.path_info)


class ProspectiveView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get_counselor(self):

        user = self.request.user
        try:
            found_counselor = user_models.Counselor.objects.get(user=user)
        except user_models.Counselor.DoesNotExist:
            return HttpResponse(status=401)

        return found_counselor

    def search(self):

        if self.request.user.type == 'counselor':
            found_counselor = self.get_counselor()
            queryset = form_models.Counsel.objects.filter(
                counselor=found_counselor, student__school__isnull=True)
        elif self.request.user.type == 'agency_branch_admin':
            found_agent_branch_admin = user_models.AgencyAdminUser.objects.get(user=self.request.user)
            found_counselors = user_models.Counselor.objects.filter(agency=found_agent_branch_admin.agency)
            queryset = form_models.Counsel.objects.filter(
                counselor__in=found_counselors, student__school__isnull=True)
        elif self.request.user.type == 'agency_admin':
            found_agent_admin = user_models.AgencyHeadAdminUser.objects.get(user=self.request.user)
            found_counselors = user_models.Counselor.objects.filter(agency__head=found_agent_admin.agency_head)
            queryset = form_models.Counsel.objects.filter(
                counselor__in=found_counselors, student__school__isnull=True)
        else:
            queryset = form_models.Counsel.objects.filter(student__school__isnull=True)

        query = self.request.GET.get('q', None)
        if query:
            queryset = queryset.filter(Q(student__name__icontains=query) |
                Q(student__email__icontains=query) |
                Q(student__phone__icontains=query)
            )

        registered = self.request.GET.get('registered', None)
        if registered:
            queryset = queryset.filter(Q(student__status=registered))

        possibility = self.request.GET.get('possibility', None)
        if possibility:
            queryset = queryset.filter(Q(possibility=possibility))

        departure = self.request.GET.get('departure', None)
        if departure:
            if departure == '3m':
                queryset = queryset.filter(expected_departure__range=(datetime.now(), datetime.now()+relativedelta(months=3)))
            elif departure == '6m':
                queryset = queryset.filter(expected_departure__range=(datetime.now(), datetime.now()+relativedelta(months=6)))
            elif departure == '12m':
                queryset = queryset.filter(expected_departure__range=(datetime.now(), datetime.now()+relativedelta(months=12)))
            else:
                queryset = queryset.filter(Q(expected_departure__gt=datetime.now()+relativedelta(years=1)))

        country = self.request.GET.get('country', None)
        if country:
            queryset = queryset.filter(Q(desire_country=country))

        program = self.request.GET.get('type', None)
        if program:
            queryset = queryset.filter(Q(program_interested=program))

        return queryset


    def get(self, request):

        found_counselor = self.get_counselor()

        all_counsel = self.search()
        paginator = Paginator(all_counsel, 10)
        page = request.GET.get('page')

        try:
            counsels = paginator.get_page(page)
        except PageNotAnInteger:
            counsels = paginator.page(1)
        except EmptyPage:
            counsels = paginator.page(paginator.num_pages)

        return render(request, 'agent/prospective.html', {"data":counsels})


class ApplicationRegisterView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get_counselor(self):

        user = self.request.user
        try:
            found_counselor = user_models.Counselor.objects.get(user=user)
        except user_models.Counselor.DoesNotExist:
            return HttpResponse(status=401)
        return found_counselor

    def get(self, request, counsel_num=None):

        if counsel_num:

            try:
                found_counsel = form_models.Counsel.objects.get(pk=counsel_num)
            except form_models.Counsel.DoesNotExist:
                return HttpResponse(status=404)

            if request.user.type == 'counselor':

                found_counselor = self.get_counselor()

                if not found_counsel.counselor == found_counselor:
                    return HttpResponse(status=401)

            try:
                student_history = student_models.StudentHistory.objects.get(student=found_counsel.student)
            except:
                student_history = None

            countries = school_models.School.objects.values('country').order_by('country').distinct()


            try:
                found_formality = form_models.Formality.objects.get(counsel=found_counsel)
                school_formalities = form_models.SchoolFormality.objects.filter(formality=found_formality).order_by('school_priority')
            except:
                school_formalities = None

            if school_formalities:
                formality_range = range(0, len(school_formalities))
                empty_range = range(len(school_formalities)+1, 11)
            else:
                formality_range = None
                empty_range = range(2, 11)

            return render(
                request,
                'agent/register.html',
                {
                    "counsel":found_counsel,
                    "student_history": student_history,
                    "countries": countries,
                    "formality_range": formality_range,
                    "empty_range": empty_range,
                    "school_formalities": school_formalities,
                })

        else:
            return HttpResponse(status=400)

    def post(self, request, counsel_num=None):

        data = request.POST
        if request.user.type == 'counselor':
            found_counselor = self.get_counselor()

        if counsel_num:
            try:
                found_counsel = form_models.Counsel.objects.get(pk=counsel_num)
            except form_models.Counsel.DoesNotExist:
                return HttpResponse(status=404)

            if request.user.type == 'counselor':
                if not found_counselor == found_counsel.counselor:
                    return HttpResponse(status=401)

            parent_info = None
            if (data.get('parentname') or data.get('parentcell') or
                    data.get('parentemail') or data.get('parentwechat')):

                try:
                    parent_info = found_counsel.student.parent_info
                    parent_info.name = data.get('parentname')
                    parent_info.phone = data.get('parentcell')
                    parent_info.email = data.get('parentemail')
                    parent_info.wechat = data.get('parentwechat')
                    parent_info.save()
                except:
                    parent_info = student_models.ParentInfo(
                        name=data.get('parentname'),
                        phone=data.get('parentcell'),
                        email=data.get('parentemail'),
                        wechat=data.get('parentwechat'),
                    )
                    parent_info.save()

            student = found_counsel.student
            if request.user.type == 'counselor':
                student.counselor=found_counselor
            student.parent_info = parent_info
            student.name = data.get('name')
            student.gender = data.get('gender')
            student.birthday = data.get('birth')
            student.email = data.get('email')
            student.skype = data.get('skype')
            student.nationality = data.get('nationality')
            student.wechat = data.get('wechat')
            student.phone = data.get('phone')
            student.save()

            image_form = student_forms.StudentImageForm(request.POST,request.FILES)
            if image_form.is_valid():
                student.image = image_form.cleaned_data['image']
                student.save()

            counsel = found_counsel
            counsel.student = student
            counsel.program_interested = data.get('program')
            counsel.expected_departure = data.get('departure')
            counsel.possibility = data.get('possibility')
            counsel.client_class = data.get('class')
            counsel.contact_first = data.get('contact1th')
            counsel.contact_second = data.get('contact2th')
            counsel.contact_third = data.get('contact3th')
            counsel.detail = data.get('detail')
            counsel.save()

            try:
                student_history = student_models.StudentHistory.objects.get(student=student)
                student_history.student = student
                student_history.current_grade = data.get('currentgrade')
                student_history.current_school=data.get('currentschool')
                student_history.apply_grade=data.get('gradeapply')
                student_history.eng_level=data.get('englevel')
                student_history.toefl=data.get('toefl')
                student_history.toefljr=data.get('toefljr')
                student_history.gpa=data.get('gpa')
                student_history.sat=data.get('sat')
                student_history.address=data.get('address')
                student_history.save()

            except student_models.StudentHistory.DoesNotExist:
                student_history = student_models.StudentHistory(
                    student=student,
                    current_grade=data.get('currentgrade'),
                    current_school=data.get('currentschool'),
                    apply_grade=data.get('gradeapply'),
                    eng_level=data.get('englevel'),
                    toefl=data.get('toefl'),
                    toefljr=data.get('toefljr'),
                    gpa=data.get('gpa'),
                    sat=data.get('sat'),
                    address=data.get('address'),
                )
                student_history.save()

            school_ids = []
            class_start_days = []
            courses = []
            for i in range(1,11):
                if data.get('app_school'+str(i)):
                    school_ids.append(data.get('app_school'+str(i)))
                    class_start_days.append(data.get('app_start'+str(i)))
                    courses.append(data.get('app_course'+str(i)))
                else:
                    continue

            if school_ids[0]:

                # Update SchoolFormality by exsisting Formality
                try:
                    formality = form_models.Formality.objects.get(counsel=counsel)
                    school_formalities = form_models.SchoolFormality.objects.filter(formality=formality)
                    school_formalities.delete()

                 #Create Formality and SchoolFormality
                except form_models.Formality.DoesNotExist:

                    student.status = 'registered'
                    student.save()

                    formality = form_models.Formality(
                        counsel=counsel,
                        payment_complete=False,
                    )
                    formality.save()

                for index, (school, class_start_day, course) in enumerate(zip(school_ids, class_start_days, courses)):

                    try:
                        found_school = school_models.School.objects.get(pk=int(school))
                    except school_models.School.DoesNotExist:
                        return HttpResponse(status=404)

                    school_formality = form_models.SchoolFormality(
                        formality=formality,
                        school=found_school,
                        school_priority=int(index+1),
                        class_start_at=class_start_day if class_start_day else None,
                        course=course if course else None,
                    )
                    school_formality.save()


            else:
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=400)

        return HttpResponseRedirect(request.path_info)


class ProcessView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get_counselor(self):

        user = self.request.user
        try:
            found_counselor = user_models.Counselor.objects.get(user=user)
        except user_models.Counselor.DoesNotExist:
            return HttpResponse(status=401)
        return found_counselor

    def get(self, request):

        if request.user.type == 'counselor':
            found_counselor = self.get_counselor()
            found_formalities = form_models.Formality.objects.filter(
                counsel__counselor=found_counselor)
        elif request.user.type == 'agency_branch_admin':
            found_agent_branch_admin = user_models.AgencyAdminUser.objects.get(user=request.user)
            found_formalities = form_models.Formality.objects.filter(
                counsel__counselor__agency=found_agent_branch_admin.agency)
        elif request.user.type == 'agency_admin':
            found_agent_admin = user_models.AgencyHeadAdminUser.objects.get(user=request.user)
            found_formalities = form_models.Formality.objects.filter(
                counsel__counselor__agency__head=found_agent_admin.agency_head)
        else:
            found_formalities = form_models.Formality.objects.all()

        found_formalities = found_formalities.filter(
            departure_confirmed=None,
            canceled_at=None
        )

        try:
            application_not_completed = found_formalities.filter(
                Q(school_formality__enrolment_apply_done__isnull=True)|
                Q(school_formality__enrolment_apply_done=False)).order_by('created_at').distinct()
        except:
            application_not_completed =None

        try:
            upcoming_school_interview = form_models.SchoolFormality.objects.filter(
                Q(school_interview_done__isnull=True)|
                Q(school_interview_done=False)).filter(formality__in=found_formalities).exclude(
                school_interview_date__isnull=True).order_by('school_interview_date').distinct()
        except:
            upcoming_school_interview = None

        try:
            pending_admission_decision = found_formalities.filter(
                school_formality__acceptance_date__isnull=True).order_by("created_at").distinct()
        except:
            pending_admission_decision=None

        try:
            pending_issue_i20 = found_formalities.filter(
                Q(school_formality__i20_completed__isnull=True)|
                Q(school_formality__i20_completed=False)).order_by("created_at").distinct()
        except:
            pending_issue_i20=None

        try:
            upcoming_visa_interview = found_formalities.filter(
                visa_reserve_date__isnull=False,
                visa_granted_date__isnull=True,
                visa_rejected_date__isnull=True).order_by('visa_reserve_date').distinct()
        except:
            upcoming_visa_interview = None

        try:
            departure_schedule = found_formalities.exclude(
                air_departure_date__isnull=True).order_by('air_departure_date').distinct()
        except:
            departure_schedule = None

        if request.user.type == 'counselor':
            found_counselor = self.get_counselor()
            in_progress = form_models.Formality.objects.filter(
                counsel__counselor=found_counselor)
            process_completed = form_models.Formality.objects.filter(
                counsel__counselor=found_counselor)
            process_canceled = form_models.Formality.objects.filter(
                counsel__counselor=found_counselor)

        elif request.user.type == 'agency_branch_admin':
            found_agent_branch_admin = user_models.AgencyAdminUser.objects.get(user=request.user)
            in_progress = form_models.Formality.objects.filter(
                counsel__counselor__agency=found_agent_branch_admin.agency)
            process_completed = form_models.Formality.objects.filter(
                counsel__counselor__agency=found_agent_branch_admin.agency)
            process_canceled = form_models.Formality.objects.filter(
                counsel__counselor__agency=found_agent_branch_admin.agency)

        elif request.user.type == 'agency_admin':
            found_agent_admin = user_models.AgencyHeadAdminUser.objects.get(user=request.user)
            in_progress = form_models.Formality.objects.filter(
                counsel__counselor__agency__head=found_agent_admin.agency_head)
            process_completed = form_models.Formality.objects.filter(
                counsel__counselor__agency__head=found_agent_admin.agency_head)
            process_canceled = form_models.Formality.objects.filter(
                counsel__counselor__agency__head=found_agent_admin.agency_head)

        else:
            in_progress = form_models.Formality.objects.all()
            process_completed = form_models.Formality.objects.all()
            process_canceled = form_models.Formality.objects.all()

        in_progress = in_progress.filter(
            departure_confirmed=None).filter(canceled_at=None).order_by("-created_at")
        process_completed = process_completed.filter(canceled_at=None).exclude(
            departure_confirmed=None).order_by("-departure_confirmed")
        process_canceled = process_canceled.exclude(
            canceled_at=None).order_by("-canceled_at")

        return render(
            request,
            'agent/process.html',
            {
                "application_not_completed": application_not_completed,
                "upcoming_school_interview": upcoming_school_interview,
                "pending_admission_decision": pending_admission_decision,
                "pending_issue_i20": pending_issue_i20,
                "upcoming_visa_interview": upcoming_visa_interview,
                "departure_schedule": departure_schedule,
                "in_progress":in_progress,
                "process_completed":process_completed,
                "process_canceled":process_canceled,
            }
        )


class ProcessApplyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get_counselor(self):

        user = self.request.user
        try:
            found_counselor = user_models.Counselor.objects.get(user=user)
        except user_models.Counselor.DoesNotExist:
            return HttpResponse(status=401)
        return found_counselor

    def get(self, request, formality_id):

        try:
            found_formality = form_models.Formality.objects.get(pk=formality_id)
        except form_models.Formality.DoesNotExist:
            return HttpResponse(status=400)

        if request.user.type == 'counselor':
            found_counselor = self.get_counselor()

            if not found_formality.counsel.counselor == found_counselor:
                return HttpResponse(status=401)

        if request.user.type == 'counselor':
            found_counselor = self.get_counselor()
            in_progress = form_models.Formality.objects.filter(
                counsel__counselor=found_counselor)
            process_completed = form_models.Formality.objects.filter(
                counsel__counselor=found_counselor)
            process_canceled = form_models.Formality.objects.filter(
                counsel__counselor=found_counselor)

        elif request.user.type == 'agency_branch_admin':
            found_agent_branch_admin = user_models.AgencyAdminUser.objects.get(user=request.user)
            in_progress = form_models.Formality.objects.filter(
                counsel__counselor__agency=found_agent_branch_admin.agency)
            process_completed = form_models.Formality.objects.filter(
                counsel__counselor__agency=found_agent_branch_admin.agency)
            process_canceled = form_models.Formality.objects.filter(
                counsel__counselor__agency=found_agent_branch_admin.agency)

        elif request.user.type == 'agency_admin':
            found_agent_admin = user_models.AgencyHeadAdminUser.objects.get(user=request.user)
            in_progress = form_models.Formality.objects.filter(
                counsel__counselor__agency__head=found_agent_admin.agency_head)
            process_completed = form_models.Formality.objects.filter(
                counsel__counselor__agency__head=found_agent_admin.agency_head)
            process_canceled = form_models.Formality.objects.filter(
                counsel__counselor__agency__head=found_agent_admin.agency_head)

        else:
            in_progress = form_models.Formality.objects.all()
            process_completed = form_models.Formality.objects.all()
            process_canceled = form_models.Formality.objects.all()

        in_progress = in_progress.filter(
            departure_confirmed=None).filter(canceled_at=None).order_by("-created_at")
        process_completed = process_completed.filter(canceled_at=None).exclude(
            departure_confirmed=None).order_by("-departure_confirmed")
        process_canceled = process_canceled.exclude(
            canceled_at=None).order_by("-canceled_at")

        student_info = found_formality.counsel.student
        student_history = student_info.student_history
        school_formalities = form_models.SchoolFormality.objects.filter(formality=found_formality).order_by('school_priority')
        formality_form = forms.FormalityForm
        formset_init = form_models.FormalityFile.objects.filter(formality=found_formality).order_by('-created_at')
        file_formset = forms.FileFormset()
        datetime_form = forms.DateTimeForm
        cancel_enrolment_form = forms.CancelEnrolmentForm
        visa_interview_scheduling_form = forms.VisaReserveSchedulingForm(instance=found_formality)
        visa_granted_form = forms.VisaGrantedForm(instance=found_formality)
        visa_rejected_form = forms.VisaRejectedForm(instance=found_formality)
        flight_departure_form = forms.FlightDepartureForm(instance=found_formality)
        flight_arrive_form = forms.FlightArriveForm(instance=found_formality)

        return render(
            request,
            'agent/formality.html',
            {
                "found_formality":found_formality,
                "in_progress":in_progress,
                "process_completed":process_completed,
                "process_canceled":process_canceled,
                "student_info":student_info,
                "student_history":student_history,
                "school_formalities":school_formalities,
                "formality_form":formality_form,
                "formset_init":formset_init,
                "file_formset":file_formset,
                "datetime_form":datetime_form,
                'cancel_enrolment_form':cancel_enrolment_form,
                "visa_interview_scheduling_form":visa_interview_scheduling_form,
                "visa_granted_form": visa_granted_form,
                "visa_rejected_form": visa_rejected_form,
                "flight_departure_form": flight_departure_form,
                "flight_arrive_form": flight_arrive_form,
            }
        )


    def post(self, request, formality_id):

        try:
            found_formality = form_models.Formality.objects.get(pk=formality_id)
        except form_models.Formality.DoesNotExist:
            return HttpResponse(status=400)

        try:
            found_accommodation = form_models.AccommodationFormality.objects.get(formality=found_formality)
        except form_models.AccommodationFormality.DoesNotExist:
            found_accommodation = None

        if request.user.type == 'counselor':
            found_counselor = self.get_counselor()

            if not found_formality.counsel.counselor == found_counselor:
                return HttpResponse(status=401)

        data = request.POST or request.FILES
        if data:

            if data.get('type') == 'registration':
                print(data)
                school_ids = data.getlist('school_id')

                for school_id in school_ids:

                    try:
                        found_school_formality = form_models.SchoolFormality.objects.get(
                            formality=found_formality, school__id=int(school_id))
                    except form_models.SchoolFormality.DoesNotExist:
                        return HttpResponse(status=404)

                    if data.get('processing_fee_'+str(school_id)):
                        processing_fee = Decimal(data.get('processing_fee_'+str(school_id)))
                    else:
                        processing_fee = None

                    if data.get('processing_fee_done_'+str(school_id)) == 'on':
                        processing_fee_done = True
                    else:
                        processing_fee_done = False

                    found_school_formality.processing_fee = processing_fee
                    found_school_formality.processing_fee_done = processing_fee_done
                    found_school_formality.save()

                school_formalities = form_models.SchoolFormality.objects.filter(formality=found_formality)
                processing_fee_done_list = []
                for school_formality in school_formalities:
                    processing_fee_done_list.append(school_formality.processing_fee_done)

                if all(processing_fee_done_list):
                    found_formality.payment_complete=True
                    found_formality.apply_at=datetime.now()
                else:
                    found_formality.payment_complete=False

                found_formality.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'cancel_registration':

                found_formality.canceled_at = data.get('Date') if data.get('Date') else None
                found_formality.cancel_reason=data.get('cancel_reason') if data.get('cancel_reason') else None
                found_formality.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == "file_upload":
                formset = forms.FileFormset(request.POST, request.FILES)
                if formset.is_valid():
                    for form in formset:
                        name = formset.cleaned_data.get('name')
                        file_source = formset.cleaned_data.get('file_source')
                        formality_file = form_models.FormalityFile(
                            formality=found_formality,
                            name=name,
                            file_source=file_source,
                        )
                        formality_file.save()
                    return HttpResponse(status=201)
                else:
                    print(formset.errors)
                    return HttpResponse(status=400)

            elif data.get('type') == "enrolment_application":

                try:
                    found_school_formality = form_models.SchoolFormality.objects.get(pk=int(data.get('school_formality_id')))
                except form_models.SchoolFormality.DoesNotExist:
                    return HttpResponse(status=400)

                found_school_formality.prepared_passport = True if data.get('passport') else False
                found_school_formality.prepared_transcript = True if data.get('transcript') else False
                found_school_formality.prepared_eng_exams = True if data.get('eng_exams') else False
                found_school_formality.prepared_recommendation = True if data.get('recommendation') else False
                found_school_formality.prepared_essay = True if data.get('essay') else False
                found_school_formality.enrolment_apply_done = True if data.get('enrolment_apply_done') else False
                found_school_formality.enrolment_apply_fee = Decimal(data.get('enrolment_apply_fee')) if data.get('enrolment_apply_fee') else None
                found_school_formality.enrolment_apply_done_date = datetime.now() if data.get('enrolment_apply_done') else False
                found_school_formality.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == "school_interview":

                if request.user.type == 'counselor' or request.user.type == 'agency_admin' or request.user.type == 'agency_branch_admin':
                    return HttpResponse("You don't have permissions", status=401)

                try:
                    found_school_formality = form_models.SchoolFormality.objects.get(pk=int(data.get('school_formality_id')))
                except form_models.SchoolFormality.DoesNotExist:
                    return HttpResponse(status=400)

                found_school_formality.school_interview_date = data.get('school_interview_date') if data.get('school_interview_date') else None
                found_school_formality.school_interview_time = data.get('school_interview_time') if data.get('school_interview_time') else None
                found_school_formality.mock_interview = True if data.get('mock_interview') else False
                found_school_formality.school_interview_done = True if data.get('interview_done') else False
                found_school_formality.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == "accepted":

                if request.user.type == 'counselor' or request.user.type == 'agency_admin' or request.user.type == 'agency_branch_admin':
                    return HttpResponse("You don't have permissions", status=401)

                try:
                    found_school_formality = form_models.SchoolFormality.objects.get(pk=int(data.get('school_formality_id')))
                except form_models.SchoolFormality.DoesNotExist:
                    return HttpResponse(status=400)

                found_school_formality.acceptance_date = data.get('Date') if data.get('Date') else None
                found_school_formality.acceptance_letter = True if data.get('acceptance_letter') else None
                found_school_formality.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'cancel_enrolment':

                if request.user.type == 'counselor' or request.user.type == 'agency_admin' or request.user.type == 'agency_branch_admin':
                    return HttpResponse("You don't have permissions", status=401)

                try:
                    found_school_formality = form_models.SchoolFormality.objects.get(pk=int(data.get('school_formality_id')))
                except form_models.SchoolFormality.DoesNotExist:
                    return HttpResponse(status=400)

                found_school_formality.cancel_enrolment_date = data.get('cancel_enrolment_date') if data.get('cancel_enrolment_date') else None
                found_school_formality.cancel_enrolment_time = data.get('cancel_enrolment_time') if data.get('cancel_enrolment_time') else None
                found_school_formality.save()

                try:
                    found_student = student_models.Student.objects.get(counsel__formality__school_formality=found_school_formality)
                except student_models.Student.DoesNotExist:
                    return HttpResponse("Student school formality error", status=400)

                found_student.school=None
                found_student.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'i20_request':

                try:
                    found_school_formality = form_models.SchoolFormality.objects.get(pk=int(data.get('school_formality_id')))
                except form_models.SchoolFormality.DoesNotExist:
                    return HttpResponse(status=400)

                found_school_formality.i20_completed = True if data.get('i20_completed') else False
                found_school_formality.i20_fee = Decimal(data.get('i20_fee')) if data.get('i20_fee') else None
                found_school_formality.i20_receipt = True if data.get('i20_receipt') else False
                found_school_formality.save()

                if found_school_formality.i20_completed:
                    try:
                        found_student = student_models.Student.objects.get(counsel__formality__school_formality=found_school_formality)
                    except student_models.Student.DoesNotExist:
                        return HttpResponse("Student school formality error", status=400)

                    found_student.school=found_school_formality.school
                    found_student.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'i20_received':

                try:
                    found_school_formality = form_models.SchoolFormality.objects.get(pk=int(data.get('school_formality_id')))
                except form_models.SchoolFormality.DoesNotExist:
                    return HttpResponse(status=400)

                found_school_formality.i20_received_date = data.get('Date') if data.get('Date') else None
                found_school_formality.i20_copy = True if data.get('i20_copy') else False
                found_school_formality.i20_tracking = data.get('i20_tracking') if data.get('i20_tracking') else None
                found_school_formality.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'program_fee_payment':

                try:
                    found_school_formality = form_models.SchoolFormality.objects.get(pk=int(data.get('school_formality_id')))
                except form_models.SchoolFormality.DoesNotExist:
                    return HttpResponse(status=400)

                found_school_formality.provider_application = True if data.get('provider_application') else False
                found_school_formality.bge_program_application = True if data.get('bge_program_application') else False
                found_school_formality.immunization = True if data.get('immunization') else False
                found_school_formality.financial_support = True if data.get('financial_support') else False
                found_school_formality.program_fee_completed = True if data.get('program_fee_completed') else False
                found_school_formality.program_fee = Decimal(data.get('program_fee')) if data.get('program_fee') else None
                found_school_formality.program_fee_receipt = True if data.get('program_fee_receipt') else False
                found_school_formality.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'visa_interview_scheduling':

                found_formality.visa_reserve_date = data.get('visa_reserve_date') if data.get('visa_reserve_date') else None
                found_formality.visa_reserve_time = data.get('visa_reserve_time') if data.get('visa_reserve_time') else None
                found_formality.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'visa_granted':

                found_formality.visa_granted_date = data.get('visa_granted_date') if data.get('visa_granted_date') else None
                found_formality.visa_granted_time = data.get('visa_granted_time') if data.get('visa_granted_time') else None
                found_formality.visa_copy_recieved = True if data.get('visa_copy_recieved') else False
                found_formality.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'visa_rejected':

                found_formality.visa_rejected_date = data.get('visa_rejected_date') if data.get('visa_rejected_date') else None
                found_formality.visa_rejected_time = data.get('visa_rejected_time') if data.get('visa_rejected_time') else None
                found_formality.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'flight_ticketing':

                found_formality.eticket_attached = True if data.get('eticket_attached') else False
                found_formality.air_departure_date = data.get('air_departure_date') if data.get('air_departure_date') else None
                found_formality.air_departure_time = data.get('air_departure_time') if data.get('air_departure_time') else None
                found_formality.air_departure_port = data.get('air_departure_port') if data.get('air_departure_port') else None
                found_formality.air_arrive_date = data.get('air_arrive_date') if data.get('air_arrive_date') else None
                found_formality.air_arrive_time = data.get('air_arrive_time') if data.get('air_arrive_time') else None
                found_formality.air_arrive_port = data.get('air_arrive_port') if data.get('air_arrive_port') else None
                found_formality.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'airport_pickup':

                found_formality.pickup_num = data.get('pickup_num') if data.get('pickup_num') else None
                found_formality.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'accommodation_application':

                if found_accommodation:
                    found_accommodation.with_animal = True if data.get('with_animal') else False
                    found_accommodation.with_child = True if data.get('with_child') else False
                    found_accommodation.with_other_student = True if data.get('with_other_student') else False
                    found_accommodation.other_preference = data.get('other_preference') if data.get('other_preference') else None
                    found_accommodation.application_at = datetime.now()
                    found_accommodation.save()

                else:
                    accommodation = form_models.AccommodationFormality(
                        formality = found_formality,
                        with_animal = True if data.get('with_animal') else False,
                        with_child = True if data.get('with_child') else False,
                        with_other_student = True if data.get('with_other_student') else False,
                        other_preference = data.get('other_preference') if data.get('other_preference') else None,
                        application_at = datetime.now()
                    )
                    accommodation.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'homestay_recommendation':

                if found_accommodation:
                    found_accommodation.recommendation_a = request.FILES.get('recommendation_a') if request.FILES.get('recommendation_a') else None
                    found_accommodation.recommendation_b = request.FILES.get('recommendation_b') if request.FILES.get('recommendation_b') else None
                    found_accommodation.recommendation_c = request.FILES.get('recommendation_c') if request.FILES.get('recommendation_c') else None
                    found_accommodation.recommendation_a_comment = data.get('recommendation_a_comment') if data.get('recommendation_a_comment') else None
                    found_accommodation.recommendation_b_comment = data.get('recommendation_b_comment') if data.get('recommendation_b_comment') else None
                    found_accommodation.recommendation_c_comment = data.get('recommendation_c_comment') if data.get('recommendation_c_comment') else None
                    found_accommodation.homestay_recommendation_at = datetime.now()
                    found_accommodation.save()

                else:
                    accommodation = form_models.AccommodationFormality(
                        formality = found_formality,
                        recommendation_a = request.FILES.get('recommendation_a') if request.FILES.get('recommendation_a') else None,
                        recommendation_b = request.FILES.get('recommendation_b') if request.FILES.get('recommendation_b') else None ,
                        recommendation_c = request.FILES.get('recommendation_c') if request.FILES.get('recommendation_c') else None ,
                        recommendation_a_comment = data.get('recommendation_a_comment') if data.get('recommendation_a_comment') else None,
                        recommendation_b_comment = data.get('recommendation_b_comment') if data.get('recommendation_b_comment') else None,
                        recommendation_c_comment = data.get('recommendation_c_comment') if data.get('recommendation_c_comment') else None,
                        homestay_recommendation_at = datetime.now()
                    )
                    accommodation.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'host_selection':

                if found_accommodation:
                    found_accommodation.host_selection = data.get('host_selection') if data.get('host_selection') else None
                    found_accommodation.host_selection_at = datetime.now()
                    found_accommodation.save()

                else:
                    accommodation = form_models.AccommodationFormality(
                        formality = found_formality,
                        host_selection = data.get('host_selection') if data.get('host_selection') else None,
                        host_selection_at = datetime.now()
                    )
                    accommodation.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'parents_accommodation':

                if found_accommodation:
                    found_accommodation.parent_accommodation_guest_num = data.get('parent_accommodation_guest_num') if data.get('parent_accommodation_guest_num') else None
                    found_accommodation.parent_length_of_stay = data.get('parent_length_of_stay') if data.get('parent_length_of_stay') else None
                    found_accommodation.parent_other_preference = data.get('parent_other_preference') if data.get('parent_other_preference') else None
                    found_accommodation.parent_accommodation_at = datetime.now()
                    found_accommodation.save()

                else:
                    accommodation = form_models.AccommodationFormality(
                        formality = found_formality,
                        parent_accommodation_guest_num = data.get('parent_accommodation_guest_num') if data.get('parent_accommodation_guest_num') else None,
                        parent_length_of_stay = data.get('parent_length_of_stay') if data.get('parent_length_of_stay') else None,
                        parent_other_preference = data.get('parent_other_preference') if data.get('parent_other_preference') else None,
                        parent_accommodation_at = datetime.now()
                    )
                    accommodation.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'departure_ot':

                found_formality.departure_ot = data.get('Date') if data.get('Date') else None
                found_formality.save()

                return HttpResponseRedirect(request.path_info)

            elif data.get('type') == 'departure_confirmed':

                found_formality.departure_confirmed = data.get('Date') if data.get('Date') else None
                found_formality.save()

                return HttpResponseRedirect(request.path_info)

            else:
                return HttpResponse(status=400)

        else:
            return HttpResponse(status=400)


# Have to solve
@login_required(login_url='/accounts/login/')
def upload_files(request, formality_id):

    data = request.POST

    try:
        found_formality = form_models.Formality.objects.get(id=formality_id)
    except form_models.Formality.DoesNotExist:
        return HttpResponse(status=400)

    if data.getlist('delete_file'):
        for file_id in data.getlist('delete_file'):
            found_file = form_models.FormalityFile.objects.get(id=int(file_id))
            found_file.delete()

        return HttpResponseRedirect("/agent/process/"+str(formality_id))

    if request.FILES.get('file_source1') or request.FILES.get('file_source2') or request.FILES.get('file_source3') or request.FILES.get('file_source4') or request.FILES.get('file_source5'):
        file_form = form_forms.FileboxForm(request.POST,request.FILES)
        if file_form.is_valid():
            for num in range(1, 6):
                file_source = request.FILES.get('file_source'+str(num))
                if file_source:

                    formality_file = form_models.FormalityFile()
                    formality_file.formality = found_formality
                    formality_file.name = request.POST.get('filebox'+str(num))
                    formality_file.file_source = file_source
                    formality_file.save()

    else:
        return HttpResponse(status=400)

    return HttpResponseRedirect("/agent/process/"+str(formality_id))


@login_required(login_url='/accounts/login/')
def load_states(request):

    country = request.GET.get('country')
    states = school_models.Secondary.objects.filter(school__country=country).values('state').order_by('state').distinct()

    state_list = []
    for state in states:
        state_list.append(state)

    states = school_models.College.objects.filter(school__country=country).values('state').order_by('state').distinct()
    for state in states:
        state_list.append(state)

    result = json.dumps({"data":state_list})

    return HttpResponse(result, content_type="application/json")


@login_required(login_url='/accounts/login/')
def load_schools(request):

    state = request.GET.get('state')

    if school_models.Secondary.objects.filter(state__iexact=state):
        schools = school_models.School.objects.filter(secondary__state__iexact=state).order_by('name')
    elif school_models.College.objects.filter(state__iexact=state):
        schools = school_models.School.objects.filter(college__state__iexact=state).order_by('name')
    else:
        return HttpResponse(status=400)

    data = serializers.serialize("json", schools)

    return HttpResponse(data, content_type="application/json")

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.db.models import Q
from django.core import serializers
from . import models, forms
from osc_bge.users import models as user_models
from osc_bge.form import models as form_models
from osc_bge.student import models as student_models
from osc_bge.school import models as school_models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
from decimal import Decimal
from datetime import datetime


class CounselView(View):

    def get(self, request):

        return render(request, 'agent/counsel.html', {})


class CustomerRegisterView(View):

    def get_counseler(self):

        user = self.request.user
        try:
            found_counseler = user_models.Counseler.objects.get(user=user)
        except user_models.Counseler.DoesNotExist:
            return HttpResponse(status=401)
        return found_counseler

    def get(self, request, counsel_num=None):

        if counsel_num:

            try:
                found_counsel = form_models.Counsel.objects.get(pk=counsel_num)
            except form_models.Counsel.DoesNotExist:
                return HttpResponse(status=404)

            found_counseler = self.get_counseler()

            if not found_counsel.counseler == found_counseler:
                return HttpResponse(status=401)

            try:
                student_history = student_models.StudentHistory.objects.get(student=found_counsel.student)
            except:
                student_history = None
            return render(request, 'agent/register.html', {"counsel":found_counsel, "student_history": student_history})

        return render(request, 'agent/register.html', {})

    def post(self, request, counsel_num=None):

        data = request.POST
        found_counseler = self.get_counseler()

        if counsel_num:
            try:
                found_counsel = form_models.Counsel.objects.get(pk=counsel_num)
            except form_models.Counsel.DoesNotExist:
                return HttpResponse(status=404)

            if not found_counseler == found_counsel.counseler:
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
            student.counseler=found_counseler
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
                counseler=found_counseler,
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

            counsel = form_models.Counsel(
                counseler=found_counseler,
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

        return redirect('/agent/prospective')


class ProspectiveView(View):

    def get_counseler(self):

        user = self.request.user
        try:
            found_counseler = user_models.Counseler.objects.get(user=user)
        except user_models.Counseler.DoesNotExist:
            return HttpResponse(status=401)

        return found_counseler

    def search(self):

        found_counseler = self.get_counseler()
        queryset = form_models.Counsel.objects.filter(counseler=found_counseler)
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
            if departure == '7d':
                queryset = queryset.filter(Q(expected_departure__lte=datetime.now()+timedelta(days=7)))
            elif departure == '1m':
                queryset = queryset.filter(Q(expected_departure__lte=datetime.now()+relativedelta(months=1)))
            elif departure == '3m':
                queryset = queryset.filter(Q(expected_departure__lte=datetime.now()+relativedelta(months=3)))
            else:
                queryset = queryset.filter(Q(expected_departure__lte=datetime.now()+relativedelta(months=6)))

        country = self.request.GET.get('country', None)
        if country:
            queryset = queryset.filter(Q(desire_country=country))

        program = self.request.GET.get('type', None)
        if program:
            queryset = queryset.filter(Q(program_interested=program))

        return queryset


    def get(self, request):

        found_counseler = self.get_counseler()

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


class ApplicationRegisterView(View):

    def get_counseler(self):

        user = self.request.user
        try:
            found_counseler = user_models.Counseler.objects.get(user=user)
        except user_models.Counseler.DoesNotExist:
            return HttpResponse(status=401)
        return found_counseler

    def get(self, request, counsel_num=None):

        if counsel_num:

            try:
                found_counsel = form_models.Counsel.objects.get(pk=counsel_num)
            except form_models.Counsel.DoesNotExist:
                return HttpResponse(status=404)

            found_counseler = self.get_counseler()

            if not found_counsel.counseler == found_counseler:
                return HttpResponse(status=401)

            try:
                student_history = student_models.StudentHistory.objects.get(student=found_counsel.student)
            except:
                student_history = None

            countries = school_models.School.objects.values('country').order_by('country').distinct()


            try:
                found_formality = form_models.Formality.objects.get(counsel=found_counsel)
                school_formalities = form_models.SchoolFormality.objects.filter(formality=found_formality).order_by('school_priority')
                print(found_formality)
                print(school_formalities)
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
        found_counseler = self.get_counseler()

        if counsel_num:
            try:
                found_counsel = form_models.Counsel.objects.get(pk=counsel_num)
            except form_models.Counsel.DoesNotExist:
                return HttpResponse(status=404)

            if not found_counseler == found_counsel.counseler:
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
            student.counseler=found_counseler
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

        return redirect('/agent/process')


class ProcessView(View):

    def get_counseler(self):

        user = self.request.user
        try:
            found_counseler = user_models.Counseler.objects.get(user=user)
        except user_models.Counseler.DoesNotExist:
            return HttpResponse(status=401)
        return found_counseler

    def get(self, request):

        found_counseler = self.get_counseler()

        in_progress = form_models.Formality.objects.filter(
            payment_complete=False).filter(
            counsel__counseler=found_counseler).order_by("-created_at")

        return render(request, 'agent/process.html', {'in_progress':in_progress})


class ProcessApplyView(View):

    def get_counseler(self):

        user = self.request.user
        try:
            found_counseler = user_models.Counseler.objects.get(user=user)
        except user_models.Counseler.DoesNotExist:
            return HttpResponse(status=401)
        return found_counseler

    def get(self, request, formality_id):

        try:
            found_formality = form_models.Formality.objects.get(pk=formality_id)
        except form_models.Formality.DoesNotExist:
            return HttpResponse(status=400)

        found_counseler = self.get_counseler()

        if not found_formality.counsel.counseler == found_counseler:
            return HttpResponse(status=401)

        in_progress = form_models.Formality.objects.filter(
            payment_complete=False).filter(
            counsel__counseler=found_counseler).order_by("-created_at")

        student_info = found_formality.counsel.student
        student_history = student_info.student_history
        school_formalities = form_models.SchoolFormality.objects.filter(formality=found_formality).order_by('school_priority')
        formality_form = forms.FormalityForm
        formset_init = form_models.FormalityFile.objects.filter(formality=found_formality).order_by('-created_at')
        file_formset = forms.FileFormset

        return render(
            request,
            'agent/formality.html',
            {
                "found_formality":found_formality,
                "in_progress":in_progress,
                "student_info":student_info,
                "student_history":student_history,
                "school_formalities":school_formalities,
                "formality_form":formality_form,
                "formset_init":formset_init,
                "file_formset":file_formset,
            }
        )


    def post(self, request, formality_id):

        try:
            found_formality = form_models.Formality.objects.get(pk=formality_id)
        except form_models.Formality.DoesNotExist:
            return HttpResponse(status=400)

        found_counseler = self.get_counseler()

        if not found_formality.counsel.counseler == found_counseler:
            return HttpResponse(status=401)

        data = request.POST or request.FILES
        if data:
            if data.get('type') == 'registration':

                school_ids = []
                for k in data.keys():
                    if 'school_id' in k:
                        school_ids.append(data.get(k))

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

                if found_formality.canceled_at:
                    found_formality.canceled_at=None
                    found_formality.cancel_reason=None

                found_formality.save()
                data = json.dumps({
                    "apply_at":str(found_formality.apply_at.strftime("%Y-%m-%d")),
                    "school_count":found_formality.school_formality_count,
                    "payment_complete_fee":str(found_formality.payment_complete_fee),
                })
                return HttpResponse(data, content_type="application/json")

            elif data.get('type') == 'cancel_registration':

                found_formality.canceled_at=data.get('Date')
                found_formality.cancel_reason=data.get('cancel_reason')
                found_formality.payment_complete=False
                found_formality.apply_at=None

                found_formality.save()

                school_formalities = form_models.SchoolFormality.objects.filter(formality=found_formality)

                for school_formality in school_formalities:
                    school_formality.processing_fee=None
                    school_formality.processing_fee_done=False
                    school_formality.save()

                return HttpResponse(status=201)

            elif data.get('type') == "file_upload":
                print(request.POST)
                print(request.FILES)
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
                    return HttpResponse(status=400)

        else:
            return HttpResponse(status=400)


def load_states(request):

    country = request.GET.get('country')
    states = school_models.School.objects.filter(country=country).values('state').order_by('state').distinct()

    state_list = []
    for state in states:
        state_list.append(state)

    result = json.dumps({"data":state_list})

    return HttpResponse(result, content_type="application/json")

def load_schools(request):

    state = request.GET.get('state')

    schools = school_models.School.objects.filter(state__iexact=state).order_by('name')

    data = serializers.serialize("json", schools)

    return HttpResponse(data, content_type="application/json")

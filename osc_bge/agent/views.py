from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from . import models
from osc_bge.users import models as user_models
from osc_bge.form import models as form_models
from osc_bge.student import models as student_models

class CounselView(View):

    def get(self, request):

        return render(request, 'agent/counsel.html', {})


class CustomerRegisterView(View):

    def get(self, request):

        return render(request, 'agent/register.html', {})

    def post(self, request):

        user = request.user
        data = request.POST
        print(data)
        try:
            found_counseler = user_models.Counseler.objects.get(user=user)
            print(found_counseler)
        except:
            return HttpResponse(status=400)

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

        return redirect('/agent/counsel')


def statistics(request):

    return render(request, 'agent/statistics.html', {})

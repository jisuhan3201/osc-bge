from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core import serializers
from . import models, forms
from osc_bge.users import models as user_models
from osc_bge.form import models as form_models
from osc_bge.school import models as school_models
from osc_bge.bge import models as bge_models
from osc_bge.branch import models as branch_models
from osc_bge.student import models as student_models
import datetime
from dateutil import relativedelta
import json

# Create your views here.

class CurrentStudentView(View):

    def get_counselor(self):

        user = self.request.user
        try:
            found_counselor = user_models.Counselor.objects.get(user=user)
        except user_models.Counselor.DoesNotExist:
            return HttpResponse(status=401)
        return found_counselor

    def get(self, request):

        found_counselor = self.get_counselor()

        try:
            current_students = models.Student.objects.filter(
                counselor=found_counselor).filter(
                counsel__formality__departure_confirmed__isnull=False).order_by('-counsel__formality__departure_confirmed')
        except models.Student.DoesNotExist:
            current_students = None

        if current_students:
            for student in current_students:

                try:
                    found_reports = models.StudentMonthlyReport.objects.filter(student=student, send_to_agent_date__isnull=False).order_by('-send_to_agent_date')
                except models.StudentMonthlyReport.DoesNotExist:
                    found_reports = None

                student.found_report = found_reports.latest('-send_to_agent_date') if found_reports else None

        return render(request, 'student/current_student.html', {
            'current_students':current_students
        })


# Agent Student report view
class StudentReportView(View):

    def get(self, request, student_id=None):

        if student_id:

            try:
                found_student = models.Student.objects.get(id=int(student_id))
            except models.Student.DoesNotExist:
                return HttpResponse('Wrong Student Id', status=404)

            all_reports = models.StudentMonthlyReport.objects.filter(
                student=found_student, send_to_agent_date__isnull=False).order_by('-send_to_agent_date')
            if all_reports:

                found_report = all_reports.latest('send_to_agent_date')

            else:
                all_reports = None
                found_report = None

            try:
                academic_records = models.StudentAcademicRecord.objects.filter(student=found_student)
            except models.StudentAcademicRecord.DoesNotExist:
                academic_records = None

            try:
                found_host_report = branch_models.HostStudentReport.objects.get(student_report=found_report)
            except branch_models.HostStudentReport.DoesNotExist:
                found_host_report = None

        else:
            return HttpResponse('No student id', status=400)

        all_logs = models.StudentCommunicationLog.objects.filter(student=found_report.student, updated_at__range=(
            datetime.date.today() - relativedelta.relativedelta(months=1),
            datetime.date.today() + relativedelta.relativedelta(days=1)))

        all_toefl = models.StudentToeflHistory.objects.filter(student=found_student).order_by('toefl_date')
        all_sat = models.StudentSatHistory.objects.filter(student=found_student).order_by('sat_date')
        all_act = models.StudentActHistory.objects.filter(student=found_student).order_by('act_date')


        return render(request, 'agent/student_report.html', {
            'found_report':found_report,
            'all_reports':all_reports,
            'academic_records':academic_records,
            'all_logs':all_logs,
            'found_host_report':found_host_report,
            'all_toefl':all_toefl,
            'all_sat':all_sat,
            'all_act':all_act,
        })

    def post(self, request, student_id=None):

        data = request.POST

        if data.get('report_id'):

            try:
                found_report = models.StudentMonthlyReport.objects.get(id=int(data.get('report_id')))
            except models.StudentMonthlyReport.DoesNotExist:
                return HttpResponse('Wrong report Id', status=404)

            found_report.agent_confirmed = data.get('agent_confirmed') if data.get('agent_confirmed') else None
            found_report.report_to_parent = data.get('report_to_parent') if data.get('report_to_parent') else None
            found_report.save()

        else:
            return HttpResponse('No report id', status=400)

        return HttpResponseRedirect(request.path_info)


class StudentPastReportView(LoginRequiredMixin, View):

    def get(self, request, report_id=None):

        if report_id:

            try:
                found_report = models.StudentMonthlyReport.objects.get(id=int(report_id))
            except models.StudentMonthlyReport.DoesNotExist:
                return HttpResponse('Wrong report Id', status=404)

            all_reports = models.StudentMonthlyReport.objects.filter(
                student=found_report.student, send_to_agent_date__isnull=False).order_by('-send_to_agent_date')

        else:
            return HttpResponse('No student id', status=400)

        try:
            found_host_report = branch_models.HostStudentReport.objects.get(student_report=found_report)
        except branch_models.HostStudentReport.DoesNotExist:
            found_host_report = None

        try:
            academic_records = models.StudentAcademicRecord.objects.filter(student=found_report.student)
        except models.StudentAcademicRecord.DoesNotExist:
            academic_records = None

        if academic_records:
            academic_range = range(academic_records.count() + 1, 9)
        else:
            academic_range = range(1, 9)

        all_toefl = models.StudentToeflHistory.objects.filter(student=found_report.student).order_by('toefl_date')
        all_sat = models.StudentSatHistory.objects.filter(student=found_report.student).order_by('sat_date')
        all_act = models.StudentActHistory.objects.filter(student=found_report.student).order_by('act_date')

        all_logs = models.StudentCommunicationLog.objects.filter(student=found_report.student, updated_at__range=(
            datetime.date.today() - relativedelta.relativedelta(months=1),
            datetime.date.today() + relativedelta.relativedelta(days=1)))

        return render(request, 'agent/student_report.html', {
            'found_report':found_report,
            'all_reports':all_reports,
            'academic_range': academic_range,
            'academic_records': academic_records,
            'found_host_report': found_host_report,
            'all_toefl':all_toefl,
            'all_sat':all_sat,
            'all_act':all_act,
            'all_logs': all_logs,
        })

    def post(self, request, report_id=None):

        data = request.POST

        if report_id:

            try:
                found_report = models.StudentMonthlyReport.objects.get(id=int(data.get('report_id')))
            except models.StudentMonthlyReport.DoesNotExist:
                return HttpResponse('Wrong report Id', status=404)

            found_report.agent_confirmed = data.get('agent_confirmed') if data.get('agent_confirmed') else None
            found_report.report_to_parent = data.get('report_to_parent') if data.get('report_to_parent') else None
            found_report.save()

        else:
            return HttpResponse('No report id', status=400)

        return HttpResponseRedirect(request.path_info)



class StudentMonthlyReportView(LoginRequiredMixin, View):

    def get(self, request, student_id=None):


        if student_id:

            try:
                found_student = models.Student.objects.get(id=int(student_id))
            except models.Student.DoesNotExist:
                return HttpResponse('Wrong Student Id', status=404)

            try:
                bge_branch_admin = user_models.BgeBranchAdminUser.objects.get(user=request.user)
                found_branch = bge_models.BgeBranch.objects.get(id=int(bge_branch_admin.branch.id))
            except:
                found_branch=None

            if not found_branch:
                try:
                    bge_branch_coordinator = user_models.BgeBranchCoordinator.objects.get(user=request.user)
                    found_branch = bge_models.BgeBranch.objects.get(id=int(bge_branch_coordinator.branch.id))
                except bge_models.BgeBranch.DoesNotExist:
                    return HttpResponse('Not Branch Admin or Branch coordi', status=400)

            try:
                academic_records = models.StudentAcademicRecord.objects.filter(student=found_student)
            except models.StudentAcademicRecord.DoesNotExist:
                academic_records = None

            if academic_records:
                academic_range = range(academic_records.count()+1, 9)
            else:
                academic_range = range(1, 9)


            all_toefl = models.StudentToeflHistory.objects.filter(student=found_student).order_by('toefl_date')
            all_sat = models.StudentSatHistory.objects.filter(student=found_student).order_by('sat_date')
            all_act = models.StudentActHistory.objects.filter(student=found_student).order_by('act_date')
            all_schools = school_models.School.objects.filter(provider_branch=found_branch)
            all_students = models.Student.objects.filter(school__in=all_schools)
            all_reports = models.StudentMonthlyReport.objects.filter(student=found_student).order_by('-updated_at')

        else:
            return HttpResponse('No student id', status=400)

        return render(request, 'student/monthly_report.html', {
            'found_student':found_student,
            'all_students':all_students,
            'all_reports':all_reports,
            'academic_range':academic_range,
            'academic_records':academic_records,
            "all_toefl":all_toefl,
            "all_sat":all_sat,
            "all_act":all_act,
        })

    def post(self, request, student_id=None):

        data = request.POST
        if student_id:

            try:
                found_student = models.Student.objects.get(id=int(student_id))
            except models.Student.DoesNotExist:
                return HttpResponse('Wrong Student Id', status=404)

            if request.FILES.get('image'):

                image_form = forms.StudentImageForm(request.POST,request.FILES)
                if image_form.is_valid():
                    found_student.image = image_form.cleaned_data['image']
                    found_student.save()


            report = models.StudentMonthlyReport(
                student=found_student,
                counseling_date=data.get('counseling_date'),
                school_year=data.get('school_year'),
                grade=data.get('grade'),
                college_plan=data.get('college_plan'),
                comment=data.get('comment'),
                target_gpa=data.get('target_gpa'),
                transcript=data.get('transcript'),
                eng_skill=data.get('eng_skill'),
                ap_tests=data.get('ap_tests'),
                sat_subjects_tests=data.get('sat_subjects_tests'),
                test_prep=data.get('test_prep'),
                activities=data.get('activities'),
                community_services=data.get('community_services'),
                agenda=data.get('agenda'),
                comment2=data.get('comment2'),
                objective_assignment=data.get('objective_assignment'),
                payment_desc=data.get('payment_desc'),
                payment_expense=data.get('payment_expense'),
                payment_due_date=data.get('payment_due_date'),
                payment_payment=data.get('payment_payment'),
                payment_paid_date=data.get('payment_paid_date'),
                payment_balance=data.get('payment_balance'),
                payment_invoice=data.get('payment_invoice'),
                status=data.get('status'),
                quater_gpa=data.get('quater_gpa')
            )
            report.save()

            for num in range(1, 9):

                if data.get('subject'+str(num)):
                    try:
                        academic_record = models.StudentAcademicRecord.objects.get(student=found_student, subject_number=num)
                        academic_record.subject = data.get('subject'+str(num)) if data.get('subject'+str(num)) else None
                    except models.StudentAcademicRecord.DoesNotExist:
                        academic_record = models.StudentAcademicRecord(
                            student=found_student,
                            subject_number=num,
                            subject=data.get('subject'+str(num)) if data.get('subject'+str(num)) else None
                        )

                    academic_record.save()

                if data.get('level'+str(num)):
                    try:
                        academic_record = models.StudentAcademicRecord.objects.get(student=found_student, subject_number=num)
                        academic_record.level = data.get('level'+str(num)) if data.get('level'+str(num)) else None
                    except models.StudentAcademicRecord.DoesNotExist:
                        academic_record = models.StudentAcademicRecord(
                            student=found_student,
                            subject_number=num,
                            level=data.get('level'+str(num)) if data.get('level'+str(num)) else None
                        )

                    academic_record.save()

                if data.get('target'+str(num)):
                    try:
                        academic_record = models.StudentAcademicRecord.objects.get(student=found_student, subject_number=num)
                        academic_record.target = data.get('target'+str(num)) if data.get('target'+str(num)) else None
                    except models.StudentAcademicRecord.DoesNotExist:
                        academic_record = models.StudentAcademicRecord(
                            student=found_student,
                            subject_number=num,
                            target=data.get('target'+str(num)) if data.get('target'+str(num)) else None
                        )
                    academic_record.save()

                if data.get('current'+str(num)):
                    try:
                        academic_record = models.StudentAcademicRecord.objects.get(student=found_student, subject_number=num)
                        academic_record.current = data.get('current'+str(num)) if data.get('current'+str(num)) else None
                    except models.StudentAcademicRecord.DoesNotExist:
                        academic_record = models.StudentAcademicRecord(
                            student=found_student,
                            subject_number=num,
                            current=data.get('current'+str(num)) if data.get('current'+str(num)) else None
                        )
                    academic_record.save()

                if data.get('current_grade'+str(num)):
                    try:
                        academic_record = models.StudentAcademicRecord.objects.get(student=found_student, subject_number=num)
                        academic_record.current_grade = data.get('current_grade'+str(num)) if data.get('current_grade'+str(num)) else None
                    except models.StudentAcademicRecord.DoesNotExist:
                        academic_record = models.StudentAcademicRecord(
                            student=found_student,
                            subject_number=num,
                            current_grade=data.get('current_grade'+str(num)) if data.get('current_grade'+str(num)) else None
                        )
                    academic_record.save()


            if data.getlist('toefl_id'):

                for num in data.getlist("toefl_id"):

                    try:
                        toefl = models.StudentToeflHistory.objects.get(id=num)
                    except models.StudentToeflHistory.DoesNotExist:
                        return HttpResponse('wrong toefl id', status=400)

                    toefl.toefl_date = data.get('toefl_date'+str(num)) if data.get('toefl_date'+str(num)) else None
                    toefl.reading=data.get('toefl_reading'+str(num))
                    toefl.listening=data.get('toefl_listening'+str(num))
                    toefl.speaking=data.get('toefl_speaking'+str(num))
                    toefl.writing=data.get('toefl_writing'+str(num))
                    toefl.total=data.get('toefl_total'+str(num))
                    toefl.target=data.get('toefl_target'+str(num))
                    toefl.next_test_date=data.get('toefl_next_test_date'+str(num))
                    toefl.save()

            if data.get('toefl_date'):

                toefl = models.StudentToeflHistory(
                    student=found_student,
                    toefl_date=data.get('toefl_date') if data.get('toefl_date') else None,
                    reading=data.get('toefl_reading') if data.get('toefl_reading') else None,
                    listening=data.get('toefl_listening') if data.get('toefl_listening') else None,
                    speaking=data.get('toefl_speaking') if data.get('toefl_speaking') else None,
                    writing=data.get('toefl_writing') if data.get('toefl_writing') else None,
                    total=data.get('toefl_total') if data.get('toefl_total') else None,
                    target=data.get('toefl_target') if data.get('toefl_target') else None,
                    next_test_date=data.get('toefl_next_test_date') if data.get('toefl_next_test_date') else None,
                )
                toefl.save()


            if data.getlist('sat_id'):

                for num in data.getlist("sat_id"):

                    try:
                        sat = models.StudentSatHistory.objects.get(id=num)
                    except models.StudentSatHistory.DoesNotExist:
                        return HttpResponse('wrong toefl id', status=400)

                    sat.sat_date = data.get('sat_date'+str(num)) if data.get('sat_date'+str(num)) else None
                    sat.eb_reading_writing = data.get('sat_eb_reading_writing'+str(num))
                    sat.math = data.get('sat_math'+str(num))
                    sat.total=data.get('sat_total'+str(num))
                    sat.target=data.get('sat_target'+str(num))
                    sat.next_test_date=data.get('sat_next_test_date'+str(num))
                    sat.save()

            if data.get('sat_date'):

                sat = models.StudentSatHistory(
                    student=found_student,
                    sat_date=data.get('sat_date') if data.get('sat_date') else None,
                    eb_reading_writing=data.get('sat_eb_reading_writing') if data.get('sat_eb_reading_writing') else None,
                    math=data.get('sat_math') if data.get('sat_math') else None,
                    total=data.get('sat_total') if data.get('sat_total') else None,
                    target=data.get('sat_target') if data.get('sat_target') else None,
                    next_test_date=data.get('sat_next_test_date') if data.get('sat_next_test_date') else None,
                )
                sat.save()


            if data.getlist('act_id'):

                for num in data.getlist("act_id"):

                    try:
                        act = models.StudentActHistory.objects.get(id=num)
                    except models.StudentActHistory.DoesNotExist:
                        return HttpResponse('wrong toefl id', status=400)

                    act.act_date = data.get('act_date'+str(num)) if data.get('act_date'+str(num)) else None
                    act.eng=data.get('act_eng'+str(num))
                    act.math=data.get('act_math'+str(num))
                    act.reading=data.get('act_reading'+str(num))
                    act.science=data.get('act_science'+str(num))
                    act.cp_score=data.get('act_cp_score'+str(num))
                    act.target=data.get('act_target'+str(num))
                    act.next_test_date=data.get('act_next_test_date'+str(num))
                    act.save()

            if data.get('act_date'):

                act = models.StudentActHistory(
                    student=found_student,
                    act_date=data.get('act_date') if data.get('act_date') else None,
                    eng=data.get('act_eng') if data.get('act_eng') else None,
                    math=data.get('act_math') if data.get('act_math') else None,
                    reading=data.get('act_reading') if data.get('act_reading') else None,
                    science=data.get('act_science') if data.get('act_science') else None,
                    cp_score=data.get('act_cp_score') if data.get('act_cp_score') else None,
                    target=data.get('act_target') if data.get('act_target') else None,
                    next_test_date=data.get('act_next_test_date') if data.get('act_next_test_date') else None,
                )
                act.save()


            if data.get('status') == 'send_to_agent':
                report.submit_date=datetime.datetime.today()
                report.save()


        else:
            return HttpResponse('No student id', status=400)

        return HttpResponseRedirect('/student/monthly/report/update/'+str(report.id))



class StudentMonthlyReportUpdateView(LoginRequiredMixin, View):

    def get(self, request, report_id=None):


        if report_id:

            try:
                found_report = models.StudentMonthlyReport.objects.get(id=int(report_id))
            except models.StudentMonthlyReport.DoesNotExist:
                return HttpResponse('Wrong Report Id', status=404)

            try:
                bge_branch_admin = user_models.BgeBranchAdminUser.objects.get(user=request.user)
                found_branch = bge_models.BgeBranch.objects.get(id=int(bge_branch_admin.branch.id))
            except:
                found_branch=None

            if not found_branch:
                try:
                    bge_branch_coordinator = user_models.BgeBranchCoordinator.objects.get(user=request.user)
                    found_branch = bge_models.BgeBranch.objects.get(id=int(bge_branch_coordinator.branch.id))
                except bge_models.BgeBranch.DoesNotExist:
                    return HttpResponse('Not Branch Admin or Branch coordi', status=400)

            all_schools = school_models.School.objects.filter(provider_branch=found_branch)
            all_students = models.Student.objects.filter(school__in=all_schools)
            all_reports = models.StudentMonthlyReport.objects.filter(student=found_report.student).order_by('-updated_at')

            start_date = datetime.date.today().replace(day=1)
            end_date = datetime.date.today() + relativedelta.relativedelta(months=1, day=1) - relativedelta.relativedelta(days=1)

            all_host_reports = branch_models.HostStudentReport.objects.filter(
                student=found_report.student)

            try:
                found_host_report = branch_models.HostStudentReport.objects.get(student_report=found_report)
            except branch_models.HostStudentReport.DoesNotExist:
                found_host_report=None

            try:
                academic_records = models.StudentAcademicRecord.objects.filter(student=found_report.student)
            except models.StudentAcademicRecord.DoesNotExist:
                academic_records = None

            if academic_records:
                academic_range = range(academic_records.count()+1, 9)
            else:
                academic_range = range(1, 9)

            all_toefl = models.StudentToeflHistory.objects.filter(student=found_report.student).order_by('toefl_date')
            all_sat = models.StudentSatHistory.objects.filter(student=found_report.student).order_by('sat_date')
            all_act = models.StudentActHistory.objects.filter(student=found_report.student).order_by('act_date')
            all_logs = models.StudentCommunicationLog.objects.filter(
                student=found_report.student,
                updated_at__range=(
                    datetime.date.today() - relativedelta.relativedelta(months=1),
                    datetime.date.today() + relativedelta.relativedelta(days=1)
                )
            )
        else:
            return HttpResponse('No student id', status=400)

        return render(request, 'student/monthly_report_update.html', {
            'all_students':all_students,
            'all_reports':all_reports,
            'found_report':found_report,
            'all_logs':all_logs,
            'all_host_reports':all_host_reports,
            'found_host_report':found_host_report,
            'academic_range':academic_range,
            'academic_records':academic_records,
            "all_toefl":all_toefl,
            "all_sat":all_sat,
            "all_act":all_act,
        })

    def post(self, request, report_id=None):

        data = request.POST

        if report_id:

            try:
                found_report = models.StudentMonthlyReport.objects.get(id=int(report_id))
            except models.StudentMonthlyReport.DoesNotExist:
                return HttpResponse('Wrong report id', status=400)

            try:
                found_student = models.Student.objects.get(id=found_report.student.id)
            except models.Student.DoesNotExist:
                return HttpResponse('Wrong student id', status=400)

            if data.get('host_form_id'):

                found_report.send_to_agent_date = datetime.date.today()
                found_report.status = 'submitted'
                found_report.save()

                try:
                    found_host_report = branch_models.HostStudentReport.objects.get(id=found_report.host_report.id)
                except branch_models.HostStudentReport.DoesNotExist:
                    found_host_report = None

                if found_host_report:
                    found_host_report.student_report=None
                    found_host_report.save()

                host_report = branch_models.HostStudentReport.objects.get(id=int(data.get('host_form_id')))
                host_report.student_report = found_report
                host_report.save()

                return HttpResponseRedirect(request.path_info)

            if request.FILES.get('image'):

                image_form = forms.StudentImageForm(request.POST,request.FILES)
                if image_form.is_valid():
                    found_report.student.image = image_form.cleaned_data['image']
                    found_report.student.save()

            found_report.counseling_date=data.get('counseling_date')
            found_report.manager_confirm_date=data.get('manager_confirm_date') if data.get('manager_confirm_date') else None
            found_report.school_year=data.get('school_year')
            found_report.grade=data.get('grade')
            found_report.college_plan=data.get('college_plan')
            found_report.comment=data.get('comment')
            found_report.target_gpa=data.get('target_gpa')
            found_report.transcript=data.get('transcript')
            found_report.eng_skill=data.get('eng_skill')
            found_report.ap_tests=data.get('ap_tests')
            found_report.sat_subjects_tests=data.get('sat_subjects_tests')
            found_report.test_prep=data.get('test_prep')
            found_report.activities=data.get('activities')
            found_report.community_services=data.get('community_services')
            found_report.agenda=data.get('agenda')
            found_report.comment2=data.get('comment2')
            found_report.objective_assignment=data.get('objective_assignment')
            found_report.payment_desc=data.get('payment_desc')
            found_report.payment_expense=data.get('payment_expense')
            found_report.payment_due_date=data.get('payment_due_date')
            found_report.payment_payment=data.get('payment_payment')
            found_report.payment_paid_date=data.get('payment_paid_date')
            found_report.payment_balance=data.get('payment_balance')
            found_report.payment_invoice=data.get('payment_invoice')
            found_report.status=data.get('status')
            found_report.quater_gpa=data.get('quater_gpa')

            if data.get('status') == 'send_to_agent':
                found_report.submit_date=datetime.datetime.today()

            if data.get('manager_confirm_date'):
                found_report.status = 'manager_confirmed'

            if data.get('send_to_agent_date'):
                found_report.status = 'send_to_agent'

            found_report.save()

            for num in range(1, 9):

                try:
                    academic_record = models.StudentAcademicRecord.objects.get(student=found_student, subject_number=num)
                    academic_record.subject = data.get('subject'+str(num)) if data.get('subject'+str(num)) else None
                    academic_record.level = data.get('level'+str(num)) if data.get('level'+str(num)) else None
                    academic_record.target = data.get('target'+str(num)) if data.get('target'+str(num)) else None
                    academic_record.current = data.get('current'+str(num)) if data.get('current'+str(num)) else None
                    academic_record.current_grade = data.get('current_grade'+str(num)) if data.get('current_grade'+str(num)) else None
                except models.StudentAcademicRecord.DoesNotExist:
                    academic_record = models.StudentAcademicRecord(
                        student=found_student,
                        subject_number=num,
                        subject=data.get('subject'+str(num)) if data.get('subject'+str(num)) else None,
                        level = data.get('level'+str(num)) if data.get('level'+str(num)) else None,
                        target = data.get('target'+str(num)) if data.get('target'+str(num)) else None,
                        current = data.get('current'+str(num)) if data.get('current'+str(num)) else None,
                        current_grade = data.get('current_grade'+str(num)) if data.get('current_grade'+str(num)) else None
                    )

                academic_record.save()

            if data.getlist('toefl_id'):

                for num in data.getlist("toefl_id"):

                    try:
                        toefl = models.StudentToeflHistory.objects.get(id=num)
                    except models.StudentToeflHistory.DoesNotExist:
                        return HttpResponse('wrong toefl id', status=400)

                    toefl.toefl_date = data.get('toefl_date'+str(num)) if data.get('toefl_date'+str(num)) else None
                    toefl.reading=data.get('toefl_reading'+str(num))
                    toefl.listening=data.get('toefl_listening'+str(num))
                    toefl.speaking=data.get('toefl_speaking'+str(num))
                    toefl.writing=data.get('toefl_writing'+str(num))
                    toefl.total=data.get('toefl_total'+str(num))
                    toefl.target=data.get('toefl_target'+str(num))
                    toefl.next_test_date=data.get('toefl_next_test_date'+str(num))
                    toefl.save()

            if data.get('toefl_date'):

                toefl = models.StudentToeflHistory(
                    student=found_student,
                    toefl_date=data.get('toefl_date') if data.get('toefl_date') else None,
                    reading=data.get('toefl_reading') if data.get('toefl_reading') else None,
                    listening=data.get('toefl_listening') if data.get('toefl_listening') else None,
                    speaking=data.get('toefl_speaking') if data.get('toefl_speaking') else None,
                    writing=data.get('toefl_writing') if data.get('toefl_writing') else None,
                    total=data.get('toefl_total') if data.get('toefl_total') else None,
                    target=data.get('toefl_target') if data.get('toefl_target') else None,
                    next_test_date=data.get('toefl_next_test_date') if data.get('toefl_next_test_date') else None,
                )
                toefl.save()


            if data.getlist('sat_id'):

                for num in data.getlist("sat_id"):

                    try:
                        sat = models.StudentSatHistory.objects.get(id=num)
                    except models.StudentSatHistory.DoesNotExist:
                        return HttpResponse('wrong toefl id', status=400)

                    sat.sat_date = data.get('sat_date'+str(num)) if data.get('sat_date'+str(num)) else None
                    sat.eb_reading_writing = data.get('sat_eb_reading_writing'+str(num))
                    sat.math = data.get('sat_math'+str(num))
                    sat.total=data.get('sat_total'+str(num))
                    sat.target=data.get('sat_target'+str(num))
                    sat.next_test_date=data.get('sat_next_test_date'+str(num))
                    sat.save()

            if data.get('sat_date'):

                sat = models.StudentSatHistory(
                    student=found_student,
                    sat_date=data.get('sat_date') if data.get('sat_date') else None,
                    eb_reading_writing=data.get('sat_eb_reading_writing') if data.get('sat_eb_reading_writing') else None,
                    math=data.get('sat_math') if data.get('sat_math') else None,
                    total=data.get('sat_total') if data.get('sat_total') else None,
                    target=data.get('sat_target') if data.get('sat_target') else None,
                    next_test_date=data.get('sat_next_test_date') if data.get('sat_next_test_date') else None,
                )
                sat.save()


            if data.getlist('act_id'):

                for num in data.getlist("act_id"):

                    try:
                        act = models.StudentActHistory.objects.get(id=num)
                    except models.StudentActHistory.DoesNotExist:
                        return HttpResponse('wrong toefl id', status=400)

                    act.act_date = data.get('act_date'+str(num)) if data.get('act_date'+str(num)) else None
                    act.eng=data.get('act_eng'+str(num))
                    act.math=data.get('act_math'+str(num))
                    act.reading=data.get('act_reading'+str(num))
                    act.science=data.get('act_science'+str(num))
                    act.cp_score=data.get('act_cp_score'+str(num))
                    act.target=data.get('act_target'+str(num))
                    act.next_test_date=data.get('act_next_test_date'+str(num))
                    act.save()

            if data.get('act_date'):

                act = models.StudentActHistory(
                    student=found_student,
                    act_date=data.get('act_date') if data.get('act_date') else None,
                    eng=data.get('act_eng') if data.get('act_eng') else None,
                    math=data.get('act_math') if data.get('act_math') else None,
                    reading=data.get('act_reading') if data.get('act_reading') else None,
                    science=data.get('act_science') if data.get('act_science') else None,
                    cp_score=data.get('act_cp_score') if data.get('act_cp_score') else None,
                    target=data.get('act_target') if data.get('act_target') else None,
                    next_test_date=data.get('act_next_test_date') if data.get('act_next_test_date') else None,
                )
                act.save()

        else:
            return HttpResponse('No student id', status=400)

        return HttpResponseRedirect(request.path_info)

@login_required(login_url='/accounts/login/')
def student_transcript_chart(request, student_id=None):

    if student_id:

        try:
            found_student = student_models.Student.objects.get(id=int(student_id))
        except student_models.Student.DoesNotExist:
            return HttpResponse('Wrong Student Id', status=404)

        try:
            all_sat_history = models.StudentSatHistory.objects.filter(student=found_student).order_by('sat_date')
        except models.StudentSatHistory.DoesNotExist:
            all_sat_history = None

        sat_date = []
        sat_score = []
        if all_sat_history:
            for sat in all_sat_history:

                sat_date.append(sat.sat_date)
                sat_score.append(sat.total)

        try:
            all_act_history = models.StudentActHistory.objects.filter(student=found_student).order_by('act_date')
        except models.StudentActHistory.DoesNotExist:
            all_act_history = None

        act_date = []
        act_score = []
        if all_act_history:
            for act in all_act_history:

                act_date.append(act.act_date)
                act_score.append(act.cp_score)

        try:
            all_toefl_history = models.StudentToeflHistory.objects.filter(student=found_student).order_by('toefl_date')
        except models.StudentToeflHistory.DoesNotExist:
            all_toefl_history = None

        toefl_date = []
        toefl_score = []
        if all_toefl_history:
            for toefl in all_toefl_history:

                toefl_date.append(toefl.toefl_date)
                toefl_score.append(toefl.total)


        gpa_list = []
        today = datetime.datetime.today()
        for number in range(0, 12):

            sd = today - relativedelta.relativedelta(months=number)
            ed = today - relativedelta.relativedelta(months=number-1)

            past_start_date = datetime.date(sd.year, sd.month, 1)
            past_end_date = datetime.date(ed.year, ed.month, 1)

            try:
                student_report = models.StudentMonthlyReport.objects.filter(
                    student=found_student,
                    submit_date__range=(past_start_date, past_end_date)
                ).latest('updated_at')
                gpa = student_report.quater_gpa

            except models.StudentMonthlyReport.DoesNotExist:
                gpa = 0

            try:
                gpa = float(gpa)
            except:
                gpa=0.0

            gpa_list.append(gpa)

        month_list = []
        for num in range(0, 12):

            month = datetime.datetime.today() - relativedelta.relativedelta(months=num)
            month = month.strftime("%Y %b")
            month_list.append(month)

        month_list.reverse()

    else:
        return HttpResponse(status=400)

    gpa_list.reverse()
    result = {
        'months':month_list,
        'gpa':gpa_list,
        'sat_date':sat_date,
        'sat_score':sat_score,
        'act_date':act_date,
        'act_score':act_score,
        'toefl_date':toefl_date,
        'toefl_score':toefl_score,
    }

    return JsonResponse(result, safe=False)



@login_required(login_url='/accounts/login/')
def get_host_report(request, report_id=None):

    if report_id:
        try:
            found_report = branch_models.HostStudentReport.objects.filter(id=int(report_id))
        except models.HostStudent.DoesNotExist:
            return HttpResponse(status=400)

        found_host = branch_models.HostFamily.objects.filter(id=found_report[0].host.id)
        found_photos = branch_models.ReportPhoto.objects.filter(report__id=int(report_id))
        found_files = branch_models.ReportFile.objects.filter(report__id=int(report_id))

        data = list(found_report) + list(found_host) + list(found_photos) + list(found_files)
        data = serializers.serialize("json", data)
    else:
        return HttpResponse(status=400)

    return HttpResponse(data, content_type="application/json")


class StudentCommunicationLog(LoginRequiredMixin, View):

    def get(self, request, student_id=None):

        if student_id:

            try:
                found_student = student_models.Student.objects.get(id=int(student_id))
            except student_models.Student.DoesNotExist:
                return HttpResponse('Wrong Student Id', status=404)

            try:
                bge_branch_admin = user_models.BgeBranchAdminUser.objects.get(user=request.user)
                found_branch = bge_models.BgeBranch.objects.get(id=int(bge_branch_admin.branch.id))
            except:
                found_branch=None

            if not found_branch:
                try:
                    bge_branch_coordinator = user_models.BgeBranchCoordinator.objects.get(user=request.user)
                    found_branch = bge_models.BgeBranch.objects.get(id=int(bge_branch_coordinator.branch.id))
                except bge_models.BgeBranch.DoesNotExist:
                    return HttpResponse('Not Branch Admin or Branch coordi', status=400)

            all_schools = school_models.School.objects.filter(provider_branch=found_branch)
            all_students = models.Student.objects.filter(school__in=all_schools)

            all_logs = student_models.StudentCommunicationLog.objects.filter(student=found_student).order_by('-created_at')

        else:
            return HttpResponse('No Student id', status=400)

        return render(request, 'branch/student_log.html', {
            'found_student':found_student,
            'all_logs':all_logs,
            'all_students':all_students

        })

    def post(self, request, student_id=None):

        data = request.POST

        if student_id:

            try:
                found_student = student_models.Student.objects.get(id=int(student_id))
            except student_models.Student.DoesNotExist:
                return HttpResponse('Wrong Student Id', status=404)

            if data.get('log_id'):

                try:
                    found_log = student_models.StudentCommunicationLog.objects.get(id=int(data.get('log_id')))
                except student_models.StudentCommunicationLog.DoesNotExist:
                    return HttpResponse('Wrong student id', status=400)

                found_log.writer=request.user
                found_log.category=data.get('category')
                found_log.priority=data.get('priority')
                found_log.comment=data.get('comment')
                found_log.save()

            else:

                student_log = student_models.StudentCommunicationLog(
                    student=found_student,
                    writer=request.user,
                    category=data.get('category'),
                    priority=data.get('priority'),
                    comment=data.get('comment'),
                )
                student_log.save()

        else:
            return HttpResponse('No Student id', status=400)

        return HttpResponseRedirect(request.path_info)


@login_required(login_url='/accounts/login/')
def get_student_log(request, log_id=None):

    if log_id:
        try:
            found_log = student_models.StudentCommunicationLog.objects.filter(id=int(log_id))
        except models.StudentCommunicationLog.DoesNotExist:
            return HttpResponse(status=400)

        data = serializers.serialize("json", found_log)

    else:
        return HttpResponse(status=400)

    return HttpResponse(data, content_type="application/json")

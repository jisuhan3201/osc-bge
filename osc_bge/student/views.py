from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from . import models
from osc_bge.users import models as user_models
from osc_bge.form import models as form_models
from osc_bge.school import models as school_models
from osc_bge.bge import models as bge_models
from osc_bge.branch import models as branch_models
import datetime
from dateutil import relativedelta

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

        current_students = models.Student.objects.filter(
            counselor=found_counselor).filter(
            counsel__formality__departure_confirmed__isnull=False).order_by('-counsel__formality__departure_confirmed')

        for student in current_students:
            found_reports = models.StudentMonthlyReport.objects.filter(student=student, send_to_agent_date__isnull=False).order_by('-send_to_agent_date')
            student.report_list = found_reports

        return render(request, 'student/current_student.html', {'current_students':current_students})


# Agent Student report view
class StudentReportView(View):

    def get(self, request, student_id=None):


        if student_id:

            try:
                found_student = models.Student.objects.get(id=int(student_id))
            except models.Student.DoesNotExist:
                return HttpResponse('Wrong Student Id', status=404)

            all_reports = models.StudentMonthlyReport.objects.filter(student=found_student, send_to_agent_date__isnull=False).order_by('-created_at')
            if all_reports:

                found_report = all_reports.latest('send_to_agent_date')

                start_date = datetime.date.today().replace(day=1)
                end_date = datetime.date.today() + relativedelta.relativedelta(months=1, day=1) - relativedelta.relativedelta(days=1)

                try:
                    found_host_report = branch_models.HostStudentReport.objects.filter(
                        student=found_report.student,
                        submitted_date__gte=start_date,
                        submitted_date__lte=end_date).latest("submitted_date")
                except branch_models.HostStudentReport.DoesNotExist:
                    found_host_report = None
                    
            else:
                all_reports = None
                found_report = None
                found_host_report = None

        else:
            return HttpResponse('No student id', status=400)

        return render(request, 'agent/student_report.html', {
            'found_report':found_report,
            'all_reports':all_reports,
            'found_host_report':found_host_report,
        })

    def post(self, request, student_id=None):

        data = request.POST

        if data.get('report_id'):

            try:
                found_report = models.StudentMonthlyReport.objects.get(id=int(data.get('report_id')))
            except models.StudentMonthlyReport.DoesNotExist:
                return HttpResponse('Wrong report Id', status=404)

            found_report.agent_confirmed = data.get('agent_confirmed')
            found_report.report_to_parent = data.get('report_to_parent')
            found_report.save()

        else:
            return HttpResponse('No report id', status=400)

        return HttpResponseRedirect('/student/current')


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

            all_schools = school_models.School.objects.filter(provider_branch=found_branch)
            all_students = models.Student.objects.filter(school__in=all_schools)
            all_reports = models.StudentMonthlyReport.objects.filter(student=found_student, submit_date__isnull=False).order_by('-created_at')

            # start_date = datetime.date.today().replace(day=1)
            # end_date = datetime.date.today() + relativedelta.relativedelta(months=1, day=1) - relativedelta.relativedelta(days=1)

            # found_report = models.StudentMonthlyReport.objects.filter(
            #     student=found_student,
            #     created_at__gte=start_date,
            #     created_at__lte=end_date)
            #
            # if found_report:
            #     return HttpResponseRedirect('/student/monthly/report/update/' + str(found_report[0].id))
        else:
            return HttpResponse('No student id', status=400)

        return render(request, 'student/monthly_report.html', {
            'found_student':found_student,
            'all_students':all_students,
            'all_reports':all_reports,
        })

    def post(self, request, student_id=None):

        data = request.POST

        if student_id:

            try:
                found_student = models.Student.objects.get(id=int(student_id))
            except models.Student.DoesNotExist:
                return HttpResponse('Wrong Student Id', status=404)

            report = models.StudentMonthlyReport(
                student=found_student,
                counseling_date=data.get('counseling_date'),
                school_year=data.get('school_year'),
                grade=data.get('grade'),
                college_plan=data.get('college_plan'),
                eng9h_lv=data.get('eng9h_lv'),
                eng9h_tg=data.get('eng9h_tg'),
                eng9h_current=data.get('eng9h_current'),
                precal_lv=data.get('precal_lv'),
                precal_tg=data.get('precal_tg'),
                precal_current=data.get('precal_current'),
                bioh_lv=data.get('bioh_lv'),
                bioh_tg=data.get('bioh_tg'),
                bioh_current=data.get('bioh_current'),
                chemh_lv=data.get('chemh_lv'),
                chemh_tg=data.get('chemh_tg'),
                chemh_current=data.get('chemh_current'),
                geo_lv=data.get('geo_lv'),
                geo_tg=data.get('geo_tg'),
                geo_current=data.get('geo_current'),
                cs_lv=data.get('cs_lv'),
                cs_tg=data.get('cs_tg'),
                cs_current=data.get('cs_current'),
                sp_lv=data.get('sp_lv'),
                sp_tg=data.get('sp_tg'),
                sp_current=data.get('sp_current'),
                orch_lv=data.get('orch_lv'),
                orch_tg=data.get('orch_tg'),
                orch_current=data.get('orch_current'),
                comment=data.get('comment'),
                target_gpa=data.get('target_gpa'),
                transcript=data.get('transcript'),
                eng_skill=data.get('eng_skill'),
                toefl=data.get('toefl'),
                toefl_reading=data.get('toefl_reading'),
                toefl_listening=data.get('toefl_listening'),
                toefl_speaking=data.get('toefl_speaking'),
                toefl_writing=data.get('toefl_writing'),
                toefl_total=data.get('toefl_total'),
                toefl_target=data.get('toefl_target'),
                toefl_next_test_date=data.get('toefl_next_test_date'),
                sat=data.get('sat'),
                sat_evb_reading_writing=data.get('sat_evb_reading_writing'),
                sat_math=data.get('sat_math'),
                sat_total=data.get('sat_total'),
                sat_target=data.get('sat_target'),
                sat_next_test_date=data.get('sat_next_test_date'),
                act=data.get('act'),
                act_eng=data.get('act_eng'),
                act_math=data.get('act_math'),
                act_reading=data.get('act_reading'),
                act_sci=data.get('act_sci'),
                act_composition_score=data.get('act_composition_score'),
                act_target=data.get('act_target'),
                act_next_test_date=data.get('act_next_test_date'),
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
            )
            report.save()

            if data.get('status') == 'submitted':
                report.submit_date=datetime.datetime.today()
                report.save()


        else:
            return HttpResponse('No student id', status=400)

        return HttpResponseRedirect('/branch/students')



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
            all_reports = models.StudentMonthlyReport.objects.filter(student=found_report.student, submit_date__isnull=False).order_by('-created_at')

            start_date = datetime.date.today().replace(day=1)
            end_date = datetime.date.today() + relativedelta.relativedelta(months=1, day=1) - relativedelta.relativedelta(days=1)

            try:
                found_host_report = branch_models.HostStudentReport.objects.filter(
                    student=found_report.student,
                    submitted_date__gte=start_date,
                    submitted_date__lte=end_date).latest("submitted_date")
            except branch_models.HostStudentReport.DoesNotExist:
                found_host_report = None

        else:
            return HttpResponse('No student id', status=400)

        return render(request, 'student/monthly_report_update.html', {
            'all_students':all_students,
            'all_reports':all_reports,
            'found_report':found_report,
            'found_host_report':found_host_report,
        })

    def post(self, request, report_id=None):

        data = request.POST

        if report_id:

            try:
                found_report = models.StudentMonthlyReport.objects.get(id=int(report_id))
            except models.StudentMonthlyReport.DoesNotExist:
                return HttpResponse('Wrong report id', status=400)


            found_report.counseling_date=data.get('counseling_date')
            found_report.manager_confirm_date=data.get('manager_confirm_date')
            found_report.school_year=data.get('school_year')
            found_report.grade=data.get('grade')
            found_report.send_to_agent_date=data.get('send_to_agent_date')
            found_report.college_plan=data.get('college_plan')
            found_report.eng9h_lv=data.get('eng9h_lv')
            found_report.eng9h_tg=data.get('eng9h_tg')
            found_report.eng9h_current=data.get('eng9h_current')
            found_report.precal_lv=data.get('precal_lv')
            found_report.precal_tg=data.get('precal_tg')
            found_report.precal_current=data.get('precal_current')
            found_report.bioh_lv=data.get('bioh_lv')
            found_report.bioh_tg=data.get('bioh_tg')
            found_report.bioh_current=data.get('bioh_current')
            found_report.chemh_lv=data.get('chemh_lv')
            found_report.chemh_tg=data.get('chemh_tg')
            found_report.chemh_current=data.get('chemh_current')
            found_report.geo_lv=data.get('geo_lv')
            found_report.geo_tg=data.get('geo_tg')
            found_report.geo_current=data.get('geo_current')
            found_report.cs_lv=data.get('cs_lv')
            found_report.cs_tg=data.get('cs_tg')
            found_report.cs_current=data.get('cs_current')
            found_report.sp_lv=data.get('sp_lv')
            found_report.sp_tg=data.get('sp_tg')
            found_report.sp_current=data.get('sp_current')
            found_report.orch_lv=data.get('orch_lv')
            found_report.orch_tg=data.get('orch_tg')
            found_report.orch_current=data.get('orch_current')
            found_report.comment=data.get('comment')
            found_report.target_gpa=data.get('target_gpa')
            found_report.transcript=data.get('transcript')
            found_report.eng_skill=data.get('eng_skill')
            found_report.toefl=data.get('toefl')
            found_report.toefl_reading=data.get('toefl_reading')
            found_report.toefl_listening=data.get('toefl_listening')
            found_report.toefl_speaking=data.get('toefl_speaking')
            found_report.toefl_writing=data.get('toefl_writing')
            found_report.toefl_total=data.get('toefl_total')
            found_report.toefl_target=data.get('toefl_target')
            found_report.toefl_next_test_date=data.get('toefl_next_test_date')
            found_report.sat=data.get('sat')
            found_report.sat_evb_reading_writing=data.get('sat_evb_reading_writing')
            found_report.sat_math=data.get('sat_math')
            found_report.sat_total=data.get('sat_total')
            found_report.sat_target=data.get('sat_target')
            found_report.sat_next_test_date=data.get('sat_next_test_date')
            found_report.act=data.get('act')
            found_report.act_eng=data.get('act_eng')
            found_report.act_math=data.get('act_math')
            found_report.act_reading=data.get('act_reading')
            found_report.act_sci=data.get('act_sci')
            found_report.act_composition_score=data.get('act_composition_score')
            found_report.act_target=data.get('act_target')
            found_report.act_next_test_date=data.get('act_next_test_date')
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

            if data.get('status') == 'submitted':
                found_report.submit_date=datetime.datetime.today()

            if data.get('manager_confirm_date'):
                found_report.status = 'manager_confirmed'

            if data.get('send_to_agent_date'):
                found_report.status = 'send_to_agent'

            found_report.save()

        else:
            return HttpResponse('No student id', status=400)

        return HttpResponseRedirect('/branch/students')

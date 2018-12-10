from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from . import models
from osc_bge.users import models as user_models
from osc_bge.form import models as form_models


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

        return render(request, 'student/current_student.html', {'current_students':current_students})


class StudentReportView(View):

    def get_counselor(self):

        user = self.request.user
        try:
            found_counselor = user_models.Counselor.objects.get(user=user)
        except user_models.Counselor.DoesNotExist:
            return HttpResponse(status=401)
        return found_counselor

    def get(self, request, student_id=None):

        if student_id:

            found_counselor = self.get_counselor()
            student = models.Student.objects.get(pk=int(student_id))

            current_students = models.Student.objects.filter(
                counselor=found_counselor).filter(
                counsel__formality__departure_confirmed__isnull=False).order_by('-counsel__formality__departure_confirmed')

            reports = models.StudentReport.objects.filter(student=student, counselor=found_counselor).order_by('-reported_date')

            return render(request, 'student/report.html', {
                "current_students":current_students,
                "student":student,
                'reports':reports,
            })

        else:
            return HttpResponse(status=400)


class StudentMonthlyReportView(LoginRequiredMixin, View):

    def get(self, request, student_id=None):

        if data.get('student_id'):

            try:
                found_student = student_models.Student.objects.get(id=int(data.get('student_id')))
            except student_models.Student.DoesNotExist:
                return HttpResponse('Wrong Student Id', status=404)

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

            all_schools = school_models.School.objects.filter(provider_branch=found_branch)
            all_students = student_models.Student.objects.filter(school__in=all_schools)


        else:
            return HttpResponse('No student id', status=400)

        return render(request, 'student/monthly_report.html', {})

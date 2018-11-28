from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
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

class TestReportView(View):

    def get(self, request):

        return render(request, 'student/testreport.html', {})

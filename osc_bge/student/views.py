from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from . import models
from osc_bge.users import models as user_models
from osc_bge.form import models as form_models


# Create your views here.

class CurrentStudentView(View):

    def get_counseler(self):

        user = self.request.user
        try:
            found_counseler = user_models.Counseler.objects.get(user=user)
        except user_models.Counseler.DoesNotExist:
            return HttpResponse(status=401)
        return found_counseler

    def get(self, request):

        found_counseler = self.get_counseler()

        current_students = models.Student.objects.filter(
            counseler=found_counseler).filter(
            counsel__formality__departure_confirmed__isnull=False).order_by('-counsel__formality__departure_confirmed')

        return render(request, 'student/current_student.html', {'current_students':current_students})


class StudentReportView(View):

    def get_counseler(self):

        user = self.request.user
        try:
            found_counseler = user_models.Counseler.objects.get(user=user)
        except user_models.Counseler.DoesNotExist:
            return HttpResponse(status=401)
        return found_counseler

    def get(self, request, student_id=None):

        if student_id:

            found_counseler = self.get_counseler()
            student = models.Student.objects.get(pk=int(student_id))

            current_students = models.Student.objects.filter(
                counseler=found_counseler).filter(
                counsel__formality__departure_confirmed__isnull=False).order_by('-counsel__formality__departure_confirmed')

            reports = models.StudentReport.objects.filter(student=student, counseler=found_counseler).order_by('-reported_date')

            return render(request, 'student/report.html', {
                "current_students":current_students,
                "student":student,
                'reports':reports,
            })

        else:
            return HttpResponse(status=400)

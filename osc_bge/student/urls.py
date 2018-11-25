from django.urls import path
from . import views

urlpatterns = [
    path('current', views.CurrentStudentView.as_view(), name='current_student_view'),
    path('current/<int:student_id>', views.StudentReportView.as_view(), name='student_report_view'),
]

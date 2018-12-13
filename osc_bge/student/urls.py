from django.urls import path
from . import views

urlpatterns = [
    path('current', views.CurrentStudentView.as_view(), name='current_student_view'),
    path('current/<int:student_id>', views.StudentReportView.as_view(), name='student_report_view'),
    path('current/report/<int:report_id>', views.StudentPastReportView.as_view(), name='student_past_report_view'),
    path('monthly/report/<int:student_id>', views.StudentMonthlyReportView.as_view(), name='student_monthly_report_view'),
    path('monthly/report/update/<int:report_id>', views.StudentMonthlyReportUpdateView.as_view(), name='student_monthly_report_update_view'),
    path('logs/<int:student_id>', views.StudentCommunicationLog.as_view(), name='student_communication_log'),
    path('log/get/<int:log_id>', views.get_student_log, name='get_student_log'),
    path('host/report/<int:report_id>', views.get_host_report, name='get_host_report'),
]

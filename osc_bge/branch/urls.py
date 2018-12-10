from django.urls import path
from . import views

urlpatterns = [
    path('statistics', views.BranchStatisticsView.as_view(), name='branch_statistics_view'),
    path('secondary', views.BranchSecondaryView.as_view(), name='branch_secondary_view'),
    path('students', views.BranchStudentsView.as_view(), name='branch_students_view'),
    path('hosts', views.BranchHostsView.as_view(), name='branch_hosts_view'),
    path('resources', views.BranchResourcesView.as_view(), name='branch_resources_view'),
    path('host/create', views.HostCreateView.as_view(), name='host_create_view'),
    path('host/update/<int:host_id>', views.HostUpdateView.as_view(), name='host_update_view'),
    path('host/log/<int:host_id>', views.HostLogsView.as_view(), name='host_log_view'),
    path('host/log/get/<int:log_id>', views.communication_log_get, name='get_log_ajax'),
    path('host/report/<int:student_id>', views.HostStudentReportView.as_view(), name='host_student_report_view'),
    path('host/report/update/<int:report_id>', views.HostStudentReportUpdateView.as_view(), name='host_student_report_update_view'),
]

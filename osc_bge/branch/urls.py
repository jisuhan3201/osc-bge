from django.urls import path
from . import views

urlpatterns = [
    path('statistics', views.BranchStatisticsView.as_view(), name='branch_statistics_view'),
    path('secondary', views.BranchSecondaryView.as_view(), name='branch_secondary_view'),
    path('students', views.BranchStudentsView.as_view(), name='branch_students_view'),
    path('hosts', views.BranchHostsView.as_view(), name='branch_hosts_view'),
    path('resources', views.BranchResourcesView.as_view(), name='branch_resources_view'),
    path('host/test', views.HostTestView.as_view(), name='host_test_view'),
    path('host/log', views.HostLogTestView.as_view(), name='host_log_test_view'),
    path('host/report', views.HostReportTestView.as_view(), name='host_report_test_view'),
]

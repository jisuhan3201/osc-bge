from django.urls import path
from . import views

urlpatterns = [
    path('statistics', views.BranchStatisticsView.as_view(), name='branch_statistics_view'),
    path('secondary', views.BranchSecondaryView.as_view(), name='branch_secondary_view'),
    path('students', views.BranchStudentsView.as_view(), name='branch_students_view'),
    path('hosts', views.BranchHostsView.as_view(), name='branch_hosts_view'),
    path('resources', views.BranchResourcesView.as_view(), name='branch_resources_view'),
]

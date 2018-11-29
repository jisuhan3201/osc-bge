from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('statistics', views.BgeStatisticsView.as_view(), name='bge_statistics_view'),
    path('branches', views.BranchesView.as_view(), name='branches_view'),
    path('agents', views.AgentsView.as_view(), name='agents_view'),
    path('secondary', views.SecondaryView.as_view(), name='secondary_view'),
    path('team-statistics', views.BgeTeamStatisticsView.as_view(), name='bge_team_statistics_view'),
    path('colleges', views.BgeCollegeView.as_view(), name='bge_college_view'),
]

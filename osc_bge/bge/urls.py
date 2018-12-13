from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('statistics', views.BgeStatisticsView.as_view(), name='bge_statistics_view'),
    path('branches', views.BranchesView.as_view(), name='branches_view'),
    path('branches/statistics/<int:branch_id>', views.BranchesStatisticView.as_view(), name='branches_statistics_view'),
    path('agents', views.AgentsView.as_view(), name='agents_view'),
    path('agents/info/create', views.AgentsCreateView.as_view(), name='agents_create_view'),
    path('agents/info/<int:agent_id>', views.AgentsUpdateView.as_view(), name='agents_udpate_view'),
    path('agents/info/<int:agent_id>/delete/<int:contact_id>', views.delete_contact_info, name='contact_delete_view'),
    path('agents/branch/info/<int:agent_id>', views.AgentsBranchUpdateView.as_view(), name='agents_branch_udpate_view'),
    path('agents/history/get/<int:history_id>', views.agent_history_get, name='agents_history_get_view'),
    path('secondary', views.SecondaryView.as_view(), name='secondary_view'),
    path('team-statistics', views.BgeTeamStatisticsView.as_view(), name='bge_team_statistics_view'),
    path('colleges', views.BgeCollegeView.as_view(), name='bge_college_view'),
    path('accounting', views.BgeAccountingView.as_view(), name='bge_college_view'),
]

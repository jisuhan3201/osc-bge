from django.urls import path
from . import views

urlpatterns = [
    path('secondary/test', views.SecondaryView.as_view(), name='secondary_view'),
    path('secondary/testlog', views.SecondaryLogView.as_view(), name='secondary_log_view'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('counsel', views.CounselView.as_view(), name='counselview'),
    path('statistics', views.statistics, name='statistics'),
]

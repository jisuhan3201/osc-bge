from django.urls import path
from . import views

urlpatterns = [
    path('counsel', views.CounselView.as_view(), name='counselview'),
    path('customer/register', views.CustomerRegisterView.as_view(), name='customer_register'),
    path('statistics', views.statistics, name='statistics'),
]

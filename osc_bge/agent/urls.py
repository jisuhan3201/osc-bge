from django.urls import path
from . import views

urlpatterns = [
    path('counsel', views.CounselView.as_view(), name='counselview'),
    path('prospective', views.ProspectiveView.as_view(), name='prospectiveview'),
    path('customer/register', views.CustomerRegisterView.as_view(), name='customer_register'),
    path('customer/<int:counsel_num>/register', views.CustomerRegisterView.as_view(), name='customer_update'),
    path('application/<int:counsel_num>/register', views.ApplicationRegisterView.as_view(), name='customer_application'),
    path('ajax/load-states', views.load_states, name='ajax_load_states'),
]

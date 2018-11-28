from django.urls import path
from . import views

urlpatterns = [
    path('secondary/<int:secondary_id>', views.SecondaryView.as_view(), name='secondary_view'),
]

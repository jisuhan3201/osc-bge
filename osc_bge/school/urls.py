from django.urls import path
from . import views

urlpatterns = [
    path('secondary/test', views.SecondaryView.as_view(), name='secondary_view'),
    path('secondary/testlog', views.SecondaryLogView.as_view(), name='secondary_log_view'),
    path('college/school_id', views.CollegeSchoolView.as_view(), name='college_school_view'),
    path('secondary/summary/school_id', views.SecondarySummaryView.as_view(), name='secondary_summary_view'),
    path('secondary/detail/school_id', views.SecondaryDetailView.as_view(), name='secondary_detail_view'),
    path('secondary/service/school_id', views.SecondaryServiceView.as_view(), name='secondary_service_view'),
    path('secondary/review/school_id', views.SecondaryReviewView.as_view(), name='secondary_review_view'),
    path('secondary/estimate/school_id', views.SecondaryEstimateView.as_view(), name='secondary_estimate_view'),
    path('secondary/photo/school_id', views.SecondaryPhotoView.as_view(), name='secondary_photo_view'),
]

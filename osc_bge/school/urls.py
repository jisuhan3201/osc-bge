from django.urls import path
from . import views

urlpatterns = [
    path('secondary', views.SecondaryView.as_view(), name='secondary_view'),
    path('college', views.CollegeView.as_view(), name='college_view'),
    path('secondary/create', views.SecondaryCreateView.as_view(), name='secondary_create_view'),
    path('secondary/update/<int:school_id>', views.SecondaryUpdateView.as_view(), name='secondary_update_view'),
    path('current/review', views.current_review_create, name='current_review_create'),
    path('current/review/get/<int:review_id>', views.current_review_get, name='current_review_get'),
    path('graduate/review', views.graduate_profile_create, name='graduate_profile_create'),
    path('graduate/review/get/<int:profile_id>', views.graduate_profile_get, name='graduate_profile_get'),
    path('current/review/delete/<int:review_id>', views.current_review_delete, name='current_review_delete'),
    path('graduate/review/delete/<int:review_id>', views.graduate_profile_delete, name='graduate_profile_delete'),
    path('secondary/testlog', views.SecondaryLogView.as_view(), name='secondary_log_view'),
    path('college/school_id', views.CollegeSchoolView.as_view(), name='college_school_view'),
    path('secondary/summary/<int:school_id>', views.SecondarySummaryView.as_view(), name='secondary_summary_view'),
    path('secondary/detail/<int:school_id>', views.SecondaryDetailView.as_view(), name='secondary_detail_view'),
    path('secondary/service/<int:school_id>', views.SecondaryServiceView.as_view(), name='secondary_service_view'),
    path('secondary/review/<int:school_id>', views.SecondaryReviewView.as_view(), name='secondary_review_view'),
    path('secondary/estimate/<int:school_id>', views.SecondaryEstimateView.as_view(), name='secondary_estimate_view'),
    path('secondary/photo/<int:school_id>', views.SecondaryPhotoView.as_view(), name='secondary_photo_view'),
]

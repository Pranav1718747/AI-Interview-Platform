from django.urls import path
from .views import (
    ResumeListCreateAPIView,
    ResumeDetailAPIView,
    ResumeAnalyzeAPIView,
)

urlpatterns = [
    path("", ResumeListCreateAPIView.as_view(), name="resume-list-create"),
    path("<int:pk>/", ResumeDetailAPIView.as_view(), name="resume-detail"),
    path("<int:pk>/analyze/", ResumeAnalyzeAPIView.as_view(), name="resume-analyze"),
]
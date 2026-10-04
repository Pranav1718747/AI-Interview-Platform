from django.urls import path
from .views import InterviewReportAPIView

urlpatterns = [
    path("interview/<int:pk>/", InterviewReportAPIView.as_view(), name="report-interview"),
]

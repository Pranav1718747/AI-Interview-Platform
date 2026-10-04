from django.urls import path
from .views import (
    StartInterviewAPIView,
    InterviewListAPIView,
    InterviewDetailAPIView,
    SubmitAnswerAPIView,
    FinishInterviewAPIView,
)

urlpatterns = [
    path("start/", StartInterviewAPIView.as_view(), name="interview-start"),
    path("", InterviewListAPIView.as_view(), name="interview-list"),
    path("<int:pk>/", InterviewDetailAPIView.as_view(), name="interview-detail"),
    path("<int:pk>/finish/", FinishInterviewAPIView.as_view(), name="interview-finish"),
    path("<int:session_id>/questions/<int:question_id>/answer/", SubmitAnswerAPIView.as_view(), name="interview-submit-answer"),
]

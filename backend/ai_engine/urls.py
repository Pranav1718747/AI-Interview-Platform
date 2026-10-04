from django.urls import path
from .views import AIExtractAPIView, AITestAnalyzeAPIView

urlpatterns = [
    path("extract/<int:resume_id>/", AIExtractAPIView.as_view(), name="extract-resume"),
    path("analyze-text/", AITestAnalyzeAPIView.as_view(), name="analyze-text"),
]
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from resumes.models import Resume
from .services.ai_service import analyze_resume
from .services.document_service import extract_document_text


class AIExtractAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        try:
            text = extract_document_text(resume.resume.path)
            return Response(
                {
                    "resume_id": resume.id,
                    "title": resume.title,
                    "text": text,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AITestAnalyzeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        raw_text = request.data.get("text", "")
        if not raw_text.strip():
            return Response({"error": "text field is required"}, status=status.HTTP_400_BAD_REQUEST)

        analysis = analyze_resume(raw_text)
        return Response(analysis, status=status.HTTP_200_OK)
import logging
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ai_engine.services.ai_service import analyze_resume
from ai_engine.services.document_service import extract_document_text
from .models import Resume, ResumeAnalysis
from .serializers import ResumeSerializer

logger = logging.getLogger(__name__)


def process_resume_analysis(resume_instance) -> ResumeAnalysis:
    """
    Extracts text from the resume file and analyzes it directly via OpenRouter AI.
    Raises an error if text extraction or OpenRouter fails.
    """
    file_path = resume_instance.resume.path
    extracted_text = extract_document_text(file_path)

    # Call OpenRouter LLM directly
    ai_data = analyze_resume(extracted_text)

    analysis, _ = ResumeAnalysis.objects.update_or_create(
        resume=resume_instance,
        defaults={
            "extracted_text": extracted_text,
            "summary": ai_data.get("summary", ""),
            "skills": ai_data.get("skills", []),
            "soft_skills": ai_data.get("soft_skills", []),
            "strengths": ai_data.get("strengths", []),
            "weaknesses": ai_data.get("weaknesses", []),
            "ats_score": ai_data.get("ats_score", 0),
            "suggested_roles": ai_data.get("suggested_roles", []),
            "missing_keywords": ai_data.get("missing_keywords", []),
        },
    )
    return analysis


class ResumeListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        resumes = Resume.objects.filter(user=request.user).select_related("analysis")
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            resume = serializer.save(user=request.user)
            # Run OpenRouter AI ATS analysis
            try:
                process_resume_analysis(resume)
            except Exception as e:
                logger.error(f"OpenRouter analysis error for resume {resume.id}: {e}")
                # We save the resume and return with error detail so the user knows OpenRouter state
                resume.refresh_from_db()
                return Response(
                    {
                        "resume": ResumeSerializer(resume).data,
                        "warning": f"Resume uploaded, but OpenRouter LLM failed: {str(e)}",
                    },
                    status=status.HTTP_201_CREATED,
                )

            resume.refresh_from_db()
            return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResumeDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        resume = get_object_or_404(Resume.objects.select_related("analysis"), id=pk, user=request.user)
        serializer = ResumeSerializer(resume)
        return Response(serializer.data)

    def patch(self, request, pk):
        resume = get_object_or_404(Resume, id=pk, user=request.user)
        serializer = ResumeSerializer(resume, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        resume = get_object_or_404(Resume, id=pk, user=request.user)
        resume.delete()
        return Response({"message": "Resume deleted successfully"}, status=status.HTTP_200_OK)


class ResumeAnalyzeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        resume = get_object_or_404(Resume, id=pk, user=request.user)
        try:
            process_resume_analysis(resume)
            resume.refresh_from_db()
            serializer = ResumeSerializer(resume)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"OpenRouter LLM Error: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
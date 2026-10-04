import logging
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ai_engine.services.ai_service import (
    evaluate_interview_answer,
    generate_interview_questions,
    generate_interview_summary,
)
from resumes.models import Resume
from .models import InterviewQuestion, InterviewResponse, InterviewSession
from .serializers import (
    InterviewQuestionSerializer,
    InterviewSessionDetailSerializer,
    InterviewSessionListSerializer,
    StartInterviewRequestSerializer,
    SubmitAnswerRequestSerializer,
)

logger = logging.getLogger(__name__)


class StartInterviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StartInterviewRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        role_title = data["role_title"]
        difficulty = data["difficulty"]
        interview_type = data["interview_type"]
        resume_id = data.get("resume_id")
        job_description = data.get("job_description", "")
        question_count = data.get("question_count", 5)

        resume_instance = None
        resume_context = ""
        if resume_id:
            try:
                resume_instance = Resume.objects.select_related("analysis").get(id=resume_id, user=request.user)
                if hasattr(resume_instance, "analysis") and resume_instance.analysis:
                    skills_str = ", ".join(resume_instance.analysis.skills)
                    resume_context = f"Summary: {resume_instance.analysis.summary}\nSkills: {skills_str}"
                else:
                    resume_context = f"Resume Title: {resume_instance.title}"
            except Resume.DoesNotExist:
                return Response({"error": "Selected resume not found."}, status=status.HTTP_404_NOT_FOUND)

        combined_context = f"{resume_context}\nJob Description: {job_description}".strip()

        # Call OpenRouter to generate questions directly
        try:
            generated_questions = generate_interview_questions(
                role_title=role_title,
                difficulty=difficulty,
                interview_type=interview_type,
                resume_skills_or_text=combined_context,
                count=question_count,
            )
        except Exception as e:
            logger.error(f"OpenRouter question generation error: {e}")
            return Response(
                {"error": f"OpenRouter LLM Error: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        session = InterviewSession.objects.create(
            user=request.user,
            resume=resume_instance,
            role_title=role_title,
            job_description=job_description,
            difficulty=difficulty,
            interview_type=interview_type,
            status="IN_PROGRESS",
            total_questions=len(generated_questions),
        )

        for item in generated_questions:
            InterviewQuestion.objects.create(
                session=session,
                order=item.get("order", 1),
                category=item.get("category", "TECHNICAL"),
                question_text=item.get("question_text", "Tell us about your experience."),
                expected_key_points=item.get("expected_key_points", []),
            )

        session.refresh_from_db()
        return Response(
            InterviewSessionDetailSerializer(session).data,
            status=status.HTTP_201_CREATED,
        )


class InterviewListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = InterviewSession.objects.filter(user=request.user).prefetch_related("questions__response")
        serializer = InterviewSessionListSerializer(sessions, many=True)
        return Response(serializer.data)


class InterviewDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        session = get_object_or_404(
            InterviewSession.objects.prefetch_related("questions__response"),
            id=pk,
            user=request.user,
        )
        serializer = InterviewSessionDetailSerializer(session)
        return Response(serializer.data)

    def delete(self, request, pk):
        session = get_object_or_404(InterviewSession, id=pk, user=request.user)
        session.delete()
        return Response({"message": "Interview session deleted."}, status=status.HTTP_200_OK)


class SubmitAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id, question_id):
        session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
        question = get_object_or_404(InterviewQuestion, id=question_id, session=session)

        serializer = SubmitAnswerRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        candidate_answer = serializer.validated_data["candidate_answer"]

        # Call OpenRouter directly for answer evaluation
        try:
            evaluation = evaluate_interview_answer(
                role_title=session.role_title,
                difficulty=session.difficulty,
                question_text=question.question_text,
                category=question.category,
                expected_key_points=question.expected_key_points,
                candidate_answer=candidate_answer,
            )
        except Exception as e:
            logger.error(f"OpenRouter answer evaluation error: {e}")
            return Response(
                {"error": f"OpenRouter LLM Error: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        response_obj, _ = InterviewResponse.objects.update_or_create(
            question=question,
            defaults={
                "candidate_answer": candidate_answer,
                "technical_score": evaluation.get("technical_score", 0),
                "clarity_score": evaluation.get("clarity_score", 0),
                "relevance_score": evaluation.get("relevance_score", 0),
                "overall_score": evaluation.get("overall_score", 0),
                "strengths": evaluation.get("strengths", []),
                "improvements": evaluation.get("improvements", []),
                "ideal_answer": evaluation.get("ideal_answer", ""),
                "ai_feedback": evaluation.get("ai_feedback", ""),
            },
        )

        question.refresh_from_db()
        return Response(
            InterviewQuestionSerializer(question).data,
            status=status.HTTP_200_OK,
        )


class FinishInterviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        session = get_object_or_404(
            InterviewSession.objects.prefetch_related("questions__response"),
            id=pk,
            user=request.user,
        )

        qna_records = []
        for q in session.questions.all():
            if hasattr(q, "response") and q.response:
                qna_records.append({
                    "category": q.category,
                    "question": q.question_text,
                    "answer": q.response.candidate_answer,
                    "score": q.response.overall_score,
                })

        if not qna_records:
            return Response(
                {"error": "Cannot complete interview before answering any questions."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Call OpenRouter directly for summary
        try:
            summary = generate_interview_summary(
                role_title=session.role_title,
                difficulty=session.difficulty,
                qna_records=qna_records,
            )
        except Exception as e:
            logger.error(f"OpenRouter summary error: {e}")
            return Response(
                {"error": f"OpenRouter LLM Error: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        session.overall_score = summary.get("overall_score", 0.0)
        session.technical_mastery = summary.get("technical_mastery", 0)
        session.communication_clarity = summary.get("communication_clarity", 0)
        session.problem_solving = summary.get("problem_solving", 0)
        session.readiness_rating = summary.get("readiness_rating", "Completed")
        session.key_takeaways = summary.get("key_takeaways", [])
        session.actionable_recommendations = summary.get("actionable_recommendations", [])
        session.detailed_summary = summary.get("detailed_summary", "")
        session.status = "COMPLETED"
        session.completed_at = timezone.now()
        session.save()

        session.refresh_from_db()
        return Response(
            InterviewSessionDetailSerializer(session).data,
            status=status.HTTP_200_OK,
        )

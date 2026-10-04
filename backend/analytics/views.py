from django.db.models import Avg, Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from interviews.models import InterviewSession
from resumes.models import Resume, ResumeAnalysis


class DashboardAnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Resume stats
        user_resumes = Resume.objects.filter(user=user)
        total_resumes = user_resumes.count()
        ats_stats = ResumeAnalysis.objects.filter(resume__user=user).aggregate(
            avg_ats=Avg("ats_score")
        )
        avg_ats_score = round(ats_stats["avg_ats"] or 0, 1)

        # Interview stats
        all_sessions = InterviewSession.objects.filter(user=user)
        total_interviews = all_sessions.count()
        completed_sessions = all_sessions.filter(status="COMPLETED")
        completed_count = completed_sessions.count()

        interview_stats = completed_sessions.aggregate(
            avg_overall=Avg("overall_score"),
            avg_tech=Avg("technical_mastery"),
            avg_comm=Avg("communication_clarity"),
            avg_problem=Avg("problem_solving"),
        )

        score_history = []
        for s in completed_sessions.order_by("started_at")[:10]:
            score_history.append({
                "id": s.id,
                "role_title": s.role_title,
                "difficulty": s.difficulty,
                "date": s.started_at.strftime("%b %d"),
                "overall_score": s.overall_score or 0,
                "technical": s.technical_mastery or 0,
                "communication": s.communication_clarity or 0,
                "problem_solving": s.problem_solving or 0,
            })

        recent_resumes = [
            {
                "id": r.id,
                "title": r.title,
                "uploaded_at": r.uploaded_at.strftime("%b %d, %Y"),
                "ats_score": r.analysis.ats_score if hasattr(r, "analysis") else None,
            }
            for r in user_resumes.select_related("analysis")[:4]
        ]

        recent_interviews = [
            {
                "id": s.id,
                "role_title": s.role_title,
                "difficulty": s.difficulty,
                "status": s.status,
                "overall_score": s.overall_score,
                "date": s.started_at.strftime("%b %d, %Y"),
            }
            for s in all_sessions[:4]
        ]

        return Response({
            "total_resumes": total_resumes,
            "avg_ats_score": avg_ats_score,
            "total_interviews": total_interviews,
            "completed_interviews": completed_count,
            "avg_interview_score": round(interview_stats["avg_overall"] or 0, 1),
            "skill_metrics": {
                "technical_mastery": round(interview_stats["avg_tech"] or 0, 1),
                "communication_clarity": round(interview_stats["avg_comm"] or 0, 1),
                "problem_solving": round(interview_stats["avg_problem"] or 0, 1),
            },
            "score_history": score_history,
            "recent_resumes": recent_resumes,
            "recent_interviews": recent_interviews,
        })

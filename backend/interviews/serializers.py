from rest_framework import serializers
from .models import InterviewSession, InterviewQuestion, InterviewResponse
from resumes.serializers import ResumeSerializer


class InterviewResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewResponse
        fields = [
            "id",
            "candidate_answer",
            "technical_score",
            "clarity_score",
            "relevance_score",
            "overall_score",
            "strengths",
            "improvements",
            "ideal_answer",
            "ai_feedback",
            "submitted_at",
        ]
        read_only_fields = fields


class InterviewQuestionSerializer(serializers.ModelSerializer):
    response = InterviewResponseSerializer(read_only=True)

    class Meta:
        model = InterviewQuestion
        fields = [
            "id",
            "order",
            "category",
            "question_text",
            "expected_key_points",
            "response",
        ]
        read_only_fields = fields


class InterviewSessionListSerializer(serializers.ModelSerializer):
    answered_questions_count = serializers.SerializerMethodField()

    class Meta:
        model = InterviewSession
        fields = [
            "id",
            "role_title",
            "difficulty",
            "interview_type",
            "status",
            "total_questions",
            "answered_questions_count",
            "overall_score",
            "readiness_rating",
            "started_at",
            "completed_at",
        ]
        read_only_fields = fields

    def get_answered_questions_count(self, obj):
        return sum(1 for q in obj.questions.all() if hasattr(q, "response"))


class InterviewSessionDetailSerializer(serializers.ModelSerializer):
    questions = InterviewQuestionSerializer(many=True, read_only=True)
    resume = ResumeSerializer(read_only=True)

    class Meta:
        model = InterviewSession
        fields = [
            "id",
            "role_title",
            "job_description",
            "difficulty",
            "interview_type",
            "status",
            "total_questions",
            "overall_score",
            "technical_mastery",
            "communication_clarity",
            "problem_solving",
            "readiness_rating",
            "key_takeaways",
            "actionable_recommendations",
            "detailed_summary",
            "started_at",
            "completed_at",
            "resume",
            "questions",
        ]
        read_only_fields = fields


class StartInterviewRequestSerializer(serializers.Serializer):
    role_title = serializers.CharField(max_length=255, required=True)
    difficulty = serializers.ChoiceField(
        choices=InterviewSession.DIFFICULTY_CHOICES,
        default="MID",
    )
    interview_type = serializers.ChoiceField(
        choices=InterviewSession.TYPE_CHOICES,
        default="MIXED",
    )
    resume_id = serializers.IntegerField(required=False, allow_null=True)
    job_description = serializers.CharField(required=False, allow_blank=True, default="")
    question_count = serializers.IntegerField(min_value=1, max_value=10, default=5)


class SubmitAnswerRequestSerializer(serializers.Serializer):
    candidate_answer = serializers.CharField(required=True, allow_blank=False)

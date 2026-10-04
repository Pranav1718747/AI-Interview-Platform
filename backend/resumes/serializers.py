from rest_framework import serializers
from .models import Resume, ResumeAnalysis


class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = [
            "id",
            "summary",
            "skills",
            "soft_skills",
            "strengths",
            "weaknesses",
            "ats_score",
            "suggested_roles",
            "missing_keywords",
            "created_at",
        ]
        read_only_fields = fields


class ResumeSerializer(serializers.ModelSerializer):
    analysis = ResumeAnalysisSerializer(read_only=True)

    class Meta:
        model = Resume
        fields = [
            "id",
            "title",
            "resume",
            "uploaded_at",
            "analysis",
        ]
        read_only_fields = [
            "id",
            "uploaded_at",
            "analysis",
        ]

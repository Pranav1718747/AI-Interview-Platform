from django.conf import settings
from django.db import models


class InterviewSession(models.Model):
    DIFFICULTY_CHOICES = [
        ("ENTRY", "Entry Level"),
        ("MID", "Mid Level"),
        ("SENIOR", "Senior Level"),
        ("LEAD", "Lead / Staff"),
    ]

    TYPE_CHOICES = [
        ("TECHNICAL", "Technical"),
        ("BEHAVIORAL", "Behavioral"),
        ("MIXED", "Mixed (Technical & Behavioral)"),
        ("SYSTEM_DESIGN", "System Design"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="interview_sessions",
    )
    resume = models.ForeignKey(
        "resumes.Resume",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interview_sessions",
    )
    role_title = models.CharField(max_length=255)
    job_description = models.TextField(blank=True, default="")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default="MID")
    interview_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default="MIXED")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="IN_PROGRESS")
    total_questions = models.IntegerField(default=5)

    # Aggregated post-interview feedback
    overall_score = models.FloatField(null=True, blank=True)
    technical_mastery = models.IntegerField(null=True, blank=True)
    communication_clarity = models.IntegerField(null=True, blank=True)
    problem_solving = models.IntegerField(null=True, blank=True)
    readiness_rating = models.CharField(max_length=100, blank=True, default="")
    key_takeaways = models.JSONField(default=list, blank=True)
    actionable_recommendations = models.JSONField(default=list, blank=True)
    detailed_summary = models.TextField(blank=True, default="")

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.role_title} ({self.difficulty}) - {self.user.username} - {self.status}"


class InterviewQuestion(models.Model):
    session = models.ForeignKey(
        InterviewSession,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    order = models.IntegerField(default=1)
    category = models.CharField(max_length=50, default="TECHNICAL")
    question_text = models.TextField()
    expected_key_points = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Q{self.order} [{self.category}]: {self.question_text[:50]}..."


class InterviewResponse(models.Model):
    question = models.OneToOneField(
        InterviewQuestion,
        on_delete=models.CASCADE,
        related_name="response",
    )
    candidate_answer = models.TextField()
    technical_score = models.IntegerField(default=0)
    clarity_score = models.IntegerField(default=0)
    relevance_score = models.IntegerField(default=0)
    overall_score = models.IntegerField(default=0)
    strengths = models.JSONField(default=list, blank=True)
    improvements = models.JSONField(default=list, blank=True)
    ideal_answer = models.TextField(blank=True, default="")
    ai_feedback = models.TextField(blank=True, default="")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to Q{self.question.order} - Score: {self.overall_score}"

from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from interviews.models import InterviewSession

User = get_user_model()


class InterviewAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="interviewtester",
            email="tester2@example.com",
            password="Password123!",
        )
        login_res = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "interviewtester", "password": "Password123!"},
            format="json",
        )
        self.token = login_res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    @patch("interviews.views.generate_interview_summary")
    @patch("interviews.views.evaluate_interview_answer")
    @patch("interviews.views.generate_interview_questions")
    def test_interview_full_lifecycle(self, mock_gen_q, mock_eval_ans, mock_summary):
        # 1. Setup mock question generation
        mock_gen_q.return_value = [
            {
                "order": 1,
                "category": "TECHNICAL",
                "question_text": "Explain Python concurrency models.",
                "expected_key_points": ["GIL", "Threading vs Multiprocessing", "Asyncio"],
            },
            {
                "order": 2,
                "category": "BEHAVIORAL",
                "question_text": "Describe a difficult conflict and resolution.",
                "expected_key_points": ["Communication", "Empathy", "Outcome"],
            },
        ]

        # 1. Start an interview
        start_url = reverse("interview-start")
        start_data = {
            "role_title": "Full Stack Developer",
            "difficulty": "MID",
            "interview_type": "TECHNICAL",
            "question_count": 2,
        }
        res = self.client.post(start_url, start_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        session_id = res.data["id"]
        questions = res.data["questions"]
        self.assertEqual(len(questions), 2)

        # 2. Answer question 1
        mock_eval_ans.return_value = {
            "technical_score": 88,
            "clarity_score": 90,
            "relevance_score": 85,
            "overall_score": 88,
            "strengths": ["Deep explanation of GIL"],
            "improvements": ["Could mention uvloop"],
            "ideal_answer": "An ideal answer would detail...",
            "ai_feedback": "Strong comprehensive response.",
        }

        q1 = questions[0]
        answer_url = reverse(
            "interview-submit-answer",
            kwargs={"session_id": session_id, "question_id": q1["id"]},
        )
        ans_res = self.client.post(
            answer_url,
            {"candidate_answer": "I design robust microservices using REST APIs and Docker containers with Redis caching."},
            format="json",
        )
        self.assertEqual(ans_res.status_code, status.HTTP_200_OK)
        self.assertIn("response", ans_res.data)
        self.assertEqual(ans_res.data["response"]["overall_score"], 88)

        # 3. Finish interview
        mock_summary.return_value = {
            "overall_score": 88.0,
            "readiness_rating": "Senior Ready",
            "technical_mastery": 90,
            "communication_clarity": 88,
            "problem_solving": 86,
            "key_takeaways": ["Great technical depth"],
            "actionable_recommendations": ["Refine edge case handling"],
            "detailed_summary": "Excellent performance overall.",
        }

        finish_url = reverse("interview-finish", kwargs={"pk": session_id})
        fin_res = self.client.post(finish_url, format="json")
        self.assertEqual(fin_res.status_code, status.HTTP_200_OK)
        self.assertEqual(fin_res.data["status"], "COMPLETED")
        self.assertEqual(fin_res.data["overall_score"], 88.0)

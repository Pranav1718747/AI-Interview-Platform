from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from resumes.models import Resume

User = get_user_model()


class ResumeAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="resumetester",
            email="tester@example.com",
            password="Password123!",
        )
        login_res = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "resumetester", "password": "Password123!"},
            format="json",
        )
        self.token = login_res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    @patch("resumes.views.analyze_resume")
    def test_resume_upload_and_analysis_lifecycle(self, mock_analyze):
        mock_analyze.return_value = {
            "summary": "Experienced Python Engineer",
            "skills": ["Python", "Django", "Docker"],
            "soft_skills": ["Problem Solving"],
            "strengths": ["Strong backend skills"],
            "weaknesses": ["Needs more CI/CD"],
            "ats_score": 85,
            "suggested_roles": ["Backend Developer"],
            "missing_keywords": ["Kubernetes"],
        }

        sample_content = b"John Doe\nPython Django React Developer with 4 years experience in REST APIs and Docker."
        sample_file = SimpleUploadedFile(
            "resume.txt",
            sample_content,
            content_type="text/plain",
        )

        upload_url = reverse("resume-list-create")
        response = self.client.post(
            upload_url,
            {"title": "Senior Python Resume", "resume": sample_file},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resume.objects.count(), 1)
        resume_id = response.data["id"]

        # Verify detail view
        detail_url = reverse("resume-detail", kwargs={"pk": resume_id})
        detail_res = self.client.get(detail_url)
        self.assertEqual(detail_res.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(detail_res.data.get("analysis"))
        self.assertEqual(detail_res.data["analysis"]["ats_score"], 85)

        # Delete resume
        del_res = self.client.delete(detail_url)
        self.assertEqual(del_res.status_code, status.HTTP_200_OK)
        self.assertEqual(Resume.objects.count(), 0)

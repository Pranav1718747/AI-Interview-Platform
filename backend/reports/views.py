from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from interviews.models import InterviewSession
from interviews.serializers import InterviewSessionDetailSerializer


class InterviewReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        session = get_object_or_404(
            InterviewSession.objects.prefetch_related("questions__response"),
            id=pk,
            user=request.user,
        )
        serializer = InterviewSessionDetailSerializer(session)
        return Response({
            "report_type": "INTERVIEW_PERFORMANCE_AUDIT",
            "candidate_name": request.user.get_full_name() or request.user.username,
            "session": serializer.data,
        })

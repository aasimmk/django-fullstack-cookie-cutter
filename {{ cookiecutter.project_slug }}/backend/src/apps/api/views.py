from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthAPIView(APIView):
    """Public health check for load balancers and smoke tests."""

    authentication_classes: list = []
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request) -> Response:
        return Response({"status": "ok", "service": "{{ cookiecutter.project_slug }}"})

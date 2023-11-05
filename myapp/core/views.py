from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


@extend_schema(request=None, responses=None, auth=[{}])  # type: ignore
class HealthViewSet(GenericViewSet):
    permission_classes = [AllowAny]

    @extend_schema(
        methods=["get"],
        description="Check health.",
    )
    @action(["get"], detail=False)
    def check(self, request, *args, **kwargs):
        return Response({"status": "ok"})

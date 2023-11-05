from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer

User = get_user_model()


@extend_schema(
    methods=["post"],
    description="Creates a new user.",
    auth=[{}],  # type: ignore
)
@extend_schema(methods=["get"], description="Retrieve a user with the give id.")
@extend_schema(methods=["patch", "put"], description="Update a user.")
@extend_schema(methods=["delete"], description="Delete a user.")
class UserViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_instance(self):
        return self.request.user

    # filtering/hiding user
    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    # hiding user - not used
    # def permission_denied(self, request, **kwargs):
    #     if request.user.is_authenticated and self.action in [
    #         "update",
    #         "partial_update",
    #         "list",
    #         "retrieve",
    #     ]:
    #         raise NotFound()
    #     super().permission_denied(request, **kwargs)

    @extend_schema(methods=["get"], description="Retrieve the current user.")
    @extend_schema(methods=["put", "patch"], description="Update the current user.")
    @extend_schema(methods=["delete"], description="Delete the current user.")
    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance  # type: ignore
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

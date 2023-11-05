from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from myapp.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]
        read_only_fields = ("id",)

    def validate_password(self, value: str):
        validate_password(value)

        return value

    def create(self, validated_data: dict):
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        instance: UserType = User.objects.create_user(
            username=username, password=password, **validated_data
        )

        return instance

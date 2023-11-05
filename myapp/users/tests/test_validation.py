import pytest
from rest_framework.exceptions import ValidationError

from ..models import User
from ..serializers import UserSerializer


# testing if the password validation is called.
@pytest.mark.django_db
def test_password():
    serializer = UserSerializer(
        data={
            "username": "test1",
            "author_pseudonym": "test1",
            "password": "bad",
        }
    )
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

    serializer = UserSerializer(
        data={
            "username": "test1",
            "author_pseudonym": "test1",
            "password": "Good&84^@",
        }
    )
    serializer.is_valid(raise_exception=True)
    user: User = serializer.save()

    serializer = UserSerializer(instance=user, data={"password": "bad"}, partial=True)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

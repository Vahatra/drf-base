import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from ..models import User
from ..views import UserViewSet
from .factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture(scope="module")
def api_request_factory() -> APIRequestFactory:
    return APIRequestFactory()


# testing users/me view. Returns the currently authenticated user.
def test_user_me(api_request_factory: APIRequestFactory):
    user: User = UserFactory()
    request = api_request_factory.get("users/me")
    response = UserViewSet.as_view({"get": "me"})(request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    request = api_request_factory.get("users/me")
    force_authenticate(request, user=user)
    response = UserViewSet.as_view({"get": "me"})(request)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(user.pk)

    # PUT, didn't provide body, so 400
    request = api_request_factory.put("users/me")
    force_authenticate(request, user=user)
    response = UserViewSet.as_view({"put": "me"})(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    request = api_request_factory.patch("users/me")
    force_authenticate(request, user=user)
    response = UserViewSet.as_view({"patch": "me"})(request)
    assert response.status_code == status.HTTP_200_OK

    request = api_request_factory.delete("users/me")
    force_authenticate(request, user=user)
    response = UserViewSet.as_view({"delete": "me"})(request)
    assert response.status_code == status.HTTP_204_NO_CONTENT


# testing get_queryset() in the viewset. Goes through if the authenticated user
# is the same as the requested user.
def test_get_queryset(api_request_factory: APIRequestFactory):
    user: User = UserFactory()
    request = api_request_factory.get(f"users/{user.pk}")

    force_authenticate(request, user=user)
    response = UserViewSet.as_view({"get": "retrieve"})(request, pk=user.pk)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(user.pk)

    user_b: User = UserFactory()
    force_authenticate(request, user=user_b)
    response = UserViewSet.as_view({"get": "retrieve"})(request, pk=user.pk)
    assert response.status_code == status.HTTP_404_NOT_FOUND


# testing user creation view. Doesn't require an authentication.
def test_user_create(api_request_factory: APIRequestFactory):
    request = api_request_factory.post(
        "users",
        data={
            "username": "ckirby",
            "password": "z498n398vlkhaPPd",
            "author_pseudonym": "Joshua Spencer",
        },
        format="json",
    )
    response = UserViewSet.as_view({"post": "create"})(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "ckirby"

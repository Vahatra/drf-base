import httpx
import pytest
from rest_framework import status

from .factory import UserFactory
from .utils import is_valid_uuid


@pytest.mark.api_tests
@pytest.mark.asyncio
async def test_create(client: httpx.AsyncClient):
    user = UserFactory().create()

    resp = await client.post("users/", json=user)
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.json()
    assert len(data) == 3
    assert is_valid_uuid(data["id"])
    assert data["username"] == user["username"]


@pytest.mark.api_tests
@pytest.mark.asyncio
class TestId:
    async def test_retrieve(
        self, client: httpx.AsyncClient, authenticated_user: dict[str, str]
    ):
        client.headers = {"Authorization": f"Bearer {authenticated_user['access']}"}  # type: ignore
        response = await client.get(f"users/{authenticated_user['id']}/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert data["id"] == authenticated_user["id"]
        assert data["username"] == authenticated_user["username"]

    async def test_partial_update(
        self, client: httpx.AsyncClient, authenticated_user, fake
    ):
        new_username = fake.user_name()
        client.headers = {"Authorization": f"Bearer {authenticated_user['access']}"}  # type: ignore
        response = await client.patch(
            f"users/{authenticated_user['id']}/",
            json={"username": new_username},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert data["username"] == new_username
        assert data["id"] == authenticated_user["id"]

    async def test_update(self, client: httpx.AsyncClient, authenticated_user):
        put = UserFactory().create()
        client.headers = {"Authorization": f"Bearer {authenticated_user['access']}"}  # type: ignore
        response = await client.put(f"users/{authenticated_user['id']}/", json=put)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert data["id"] == authenticated_user["id"]
        assert data["username"] == put["username"]

    async def test_destroy(self, client: httpx.AsyncClient, authenticated_user):
        client.headers = {"Authorization": f"Bearer {authenticated_user['access']}"}  # type: ignore
        response = await client.delete(f"users/{authenticated_user['id']}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = await client.get(f"users/{authenticated_user['id']}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.api_tests
@pytest.mark.asyncio
class TestMe:
    async def test_retrieve(self, client: httpx.AsyncClient, authenticated_user):
        client.headers = {"Authorization": f"Bearer {authenticated_user['access']}"}  # type: ignore
        response = await client.get("users/me/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert data["id"] == authenticated_user["id"]
        assert data["username"] == authenticated_user["username"]

    async def test_partial_update(
        self, client: httpx.AsyncClient, authenticated_user, fake
    ):
        new_username = fake.user_name()
        client.headers = {"Authorization": f"Bearer {authenticated_user['access']}"}  # type: ignore
        response = await client.patch("users/me/", json={"username": new_username})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert data["id"] == authenticated_user["id"]
        assert data["username"] == new_username

    async def test_update(self, client: httpx.AsyncClient, authenticated_user):
        put = UserFactory().create()
        client.headers = {"Authorization": f"Bearer {authenticated_user['access']}"}  # type: ignore
        response = await client.put("users/me/", json=put)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert data["id"] == authenticated_user["id"]
        assert data["username"] == put["username"]

    async def test_destroy(self, client: httpx.AsyncClient, authenticated_user):
        client.headers = {"Authorization": f"Bearer {authenticated_user['access']}"}  # type: ignore
        response = await client.delete("users/me/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = await client.get("users/me/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

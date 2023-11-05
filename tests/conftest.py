from collections.abc import AsyncGenerator

import environ
import httpx
import pytest
import pytest_asyncio
from faker import Faker

from .factory import UserFactory

env = environ.Env()


@pytest.fixture
def fake() -> Faker:
    return Faker()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    # base_url = env.str("API_TEST_BASE_URL", "http://myapp.localhost")
    base_url = env.str("API_TEST_BASE_URL", "http://localhost:8000")
    async with httpx.AsyncClient(base_url=base_url) as client:
        yield client


@pytest_asyncio.fixture
async def user(client: httpx.AsyncClient):
    user = UserFactory().create()
    response = await client.post("users/", json=user)
    data = response.json()
    user["id"] = data["id"]
    return user


@pytest_asyncio.fixture
async def authenticated_user(client: httpx.AsyncClient):
    user = UserFactory().create()
    resp_user = await client.post("users/", json=user)
    data_user = resp_user.json()
    user["id"] = data_user["id"]
    crednetials = {
        "username": user["username"],
        "password": user["password"],
    }
    resp_jwt = await client.post("jwt/create/", json=crednetials)
    data_jwt = resp_jwt.json()
    user["access"] = data_jwt["access"]
    user["refresh"] = data_jwt["refresh"]
    return user

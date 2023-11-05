import httpx
import pytest
from rest_framework import status
from rest_framework.utils.mediatypes import media_type_matches


@pytest.mark.api_tests
@pytest.mark.asyncio
async def test_content_type(client: httpx.AsyncClient):
    response = await client.get("health/")
    assert response.status_code == status.HTTP_200_OK
    assert media_type_matches("application/json", response.headers["Content-Type"])

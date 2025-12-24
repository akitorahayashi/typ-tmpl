"""API tests executed against the dockerized development stack."""

import pytest


@pytest.mark.asyncio
class TestDockerizedAPI:
    async def test_health_endpoint_returns_ok(self, async_client):
        response = await async_client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

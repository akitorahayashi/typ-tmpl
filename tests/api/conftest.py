"""API tests executed against the dockerized development stack."""

import os

import httpx
import pytest
from testcontainers.core.container import DockerContainer
from testcontainers.core.network import Network
from testcontainers.core.wait_strategies import HttpWaitStrategy


@pytest.fixture(scope="session")
def api_network():
    with Network() as network:
        yield network


@pytest.fixture(scope="session")
def api_image():
    # Use the temporary image built for API tests
    return os.environ.get("FAPI_TMPL_E2E_IMAGE", "fapi-tmpl-e2e:latest")


@pytest.fixture(scope="session")
def api_base_url(api_image, api_network):
    env = {
        "FAPI_TMPL_USE_MOCK_GREETING": "true",
    }
    api_wait_strategy = HttpWaitStrategy(8000, "/health").for_status_code(200)
    with (
        DockerContainer(image=api_image)
        .with_network(api_network)
        .with_envs(**env)
        .with_exposed_ports(8000)
        .waiting_for(api_wait_strategy)
        .with_kwargs(log_config={"type": "json-file"}) as api
    ):
        host = api.get_container_host_ip()
        port = api.get_exposed_port(8000)
        base_url = f"http://{host}:{port}"
        print(f"\n🚀 API tests running against: {base_url}")
        yield base_url


@pytest.fixture
async def async_client(api_base_url):
    async with httpx.AsyncClient(base_url=api_base_url) as client:
        yield client

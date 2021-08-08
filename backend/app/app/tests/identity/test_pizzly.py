import pytest

from app.identity import Pizzly

pytestmark = pytest.mark.asyncio


async def test_connect(pizzly: Pizzly):
    assert await pizzly.probe()

async def test_get_auth_invalid_integration(pizzly: Pizzly):
    assert await pizzly.get_auth('invalid', '') is None
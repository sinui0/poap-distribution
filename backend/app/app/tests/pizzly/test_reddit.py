import pytest

from app.identity import RedditIdentityProvider

pytestmark = pytest.mark.asyncio

async def test_get_username(reddit: RedditIdentityProvider):
    pass
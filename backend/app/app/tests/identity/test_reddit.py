import pytest

from app.identity import RedditIdentityProvider

pytestmark = pytest.mark.asyncio

async def test_get_user_id(reddit: RedditIdentityProvider):
    print(await reddit.get_user_id('6b689b00-f71a-11eb-983d-7b124c07fe05'))
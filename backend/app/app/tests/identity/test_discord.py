import pytest

from app.identity import DiscordIdentityProvider

pytestmark = pytest.mark.asyncio

async def test_get_user_id(discord: DiscordIdentityProvider):
    print(await discord.get_user_id('fbb14040-f71a-11eb-983d-7b124c07fe05'))
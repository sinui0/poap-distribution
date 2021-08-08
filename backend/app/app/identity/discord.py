from aiohttp import ClientSession

from .base import IdentityProvider
from .pizzly import pizzly

from app.core.config import settings

class DiscordIdentityProvider(IdentityProvider):

    def __init__(self):
        self.pizzly = pizzly

    async def get_user_id(self, auth_id: str):
        auth = await self.pizzly.get_auth('discord', auth_id)
        access_token = auth.payload.get('accessToken')

        async with ClientSession(headers={'User-Agent': settings.USER_AGENT, 'Authorization':f'Bearer {access_token}'}) as session:
            response = await session.get('https://discord.com/api/users/@me')
            data = await response.json()
            return data.get('id')
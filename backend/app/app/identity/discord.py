from aiohttp import ClientSession

from .base import IdentityProviderBase
from .pizzly import pizzly

from app.core.config import settings
from app.schemas.oauth_identity import OAuthUserIdentity

class DiscordIdentityProvider(IdentityProviderBase):

    async def get_user_identity(self, auth_id: str) -> OAuthUserIdentity:
        auth = await self.get_auth('discord', auth_id)
        access_token = auth.payload.get('accessToken')

        async with ClientSession(headers={'User-Agent': settings.USER_AGENT, 'Authorization':f'Bearer {access_token}'}) as session:
            response = await session.get('https://discord.com/api/users/@me')
            data = await response.json()
            return data.get('id')
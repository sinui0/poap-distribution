from aiohttp import ClientSession

from .base import IdentityProviderBase
from .exceptions import AuthenticationNotFound, InvalidAuthentication
from .pizzly import pizzly

from app.core.config import settings
from app.schemas.oauth_identity import OAuthUserIdentity

class DiscordIdentityProvider(IdentityProviderBase):

    async def get_external_user_id(self, auth_id: str) -> str:
        auth = await self.get_auth('discord', auth_id)
        if not auth:
            raise AuthenticationNotFound
        access_token = auth.payload.get('accessToken')
        if not access_token:
            raise AuthenticationNotFound

        async with ClientSession(headers={'User-Agent': settings.USER_AGENT, 'Authorization':f'Bearer {access_token}'}) as session:
            response = await session.get('https://discord.com/api/users/@me')
            if response.status != 200:
                raise InvalidAuthentication(response.text)
            data = await response.json()
            return data.get('id')
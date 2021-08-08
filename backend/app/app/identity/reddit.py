from aiohttp import ClientSession

from .base import IdentityProvider
from .pizzly import pizzly

from app.core.config import settings

class RedditIdentityProvider(IdentityProvider):

    def __init__(self):
        self.pizzly = pizzly

    async def get_user_id(self, auth_id: str):
        auth = await self.pizzly.get_auth('reddit', auth_id)
        access_token = auth.payload.get('accessToken')

        async with ClientSession(headers={'User-Agent': settings.USER_AGENT, 'Authorization':f'Bearer {access_token}'}) as session:
            response = await session.get('https://oauth.reddit.com/api/v1/me')
            data = await response.json()
            return data.get('name')
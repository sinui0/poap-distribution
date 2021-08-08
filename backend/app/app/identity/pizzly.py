from aiohttp import ClientSession, BasicAuth

from .authentication import Authentication

from app.core.config import settings

class Pizzly:

    def __init__(self):
        self.url = f'http://{settings.PIZZLY_HOST}:{settings.PIZZLY_PORT}'

    async def probe(self) -> bool:
        async with ClientSession(auth=BasicAuth(settings.PIZZLY_SECRET_KEY,'')) as session:
            async with session.get(f'{self.url}/api/') as resp:
                return resp.status == 200
        
    async def get_auth(self, integration: str, auth_id: str) -> Authentication:
        async with ClientSession(auth=BasicAuth(settings.PIZZLY_SECRET_KEY,'')) as session:
            async with session.get(f'{self.url}/api/{integration}/authentications/{auth_id}') as resp:
                if resp.status == 200:
                    return Authentication.parse_obj(await resp.json())
                else:
                    return None

pizzly = Pizzly()
from contextlib import asynccontextmanager
import logging
import sys
from datetime import datetime, timezone

import asyncpraw

from .base import IdentityProvider
from .pizzly import pizzly

from app.core.config import settings

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
for logger_name in ("asyncpraw", "asyncprawcore"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

class RedditIdentityProvider(IdentityProvider):

    def __init__(self):
        self.pizzly = pizzly

    @asynccontextmanager
    async def reddit(self, access_token: str):
        async with asyncpraw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=None,
            #client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent='web:poap-distribution:v0.1.0 (by u/Bad_Investment)',
        ) as reddit:
            reddit.auth.implicit(access_token, 3600, 'identity')
            yield reddit

    async def get_username(self, auth_id: str):
        auth = await self.pizzly.get_auth('reddit', auth_id)
        access_token = auth.payload.get('accessToken')

        async with self.reddit(access_token) as reddit:
            return await reddit.user.me()
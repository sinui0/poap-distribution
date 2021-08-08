from .pizzly import pizzly
from .authentication import Authentication
from app.models.enums import IdentityProviderName
from app.schemas.oauth_identity import OAuthUserIdentity


class IdentityProviderBase:

    def __init__(self):
        self.pizzly = pizzly

    async def get_auth(self, provider_name: IdentityProviderName, auth_id: str) -> Authentication:
        return await self.pizzly.get_auth(provider_name, auth_id)

    async def get_user_identity(self, *, auth_id: str) -> OAuthUserIdentity:
        pass
from .base import IdentityProvider
from .pizzly import Pizzly, Token, Authentication
from .reddit import RedditIdentityProvider
from .discord import DiscordIdentityProvider

provider_map = {
    'reddit': RedditIdentityProvider(),
    'discord': DiscordIdentityProvider()
}

def get_identity_provider(provider_name: str):
    return provider_map.get(provider_name)
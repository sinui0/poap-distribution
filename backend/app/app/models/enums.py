from enum import Enum

class IdentityProviderName(str, Enum):
    reddit: str = 'reddit'
    discord: str  = 'discord'
    twitter: str = 'twitter'
    ethereum: str = 'ethereum'
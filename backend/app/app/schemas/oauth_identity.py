from typing import Optional

from pydantic import BaseModel

from datetime import datetime

from app.models.enums import IdentityProviderName


# Shared properties
class OAuthUserIdentityBase(BaseModel):
    provider: IdentityProviderName
    external_user_id: int
    user_id: Optional[int] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None


# Properties to receive via API on creation
class OAuthUserIdentityCreate(OAuthUserIdentityBase):
    pass


# Properties to receive via API on update
class OAuthUserIdentityUpdate(OAuthUserIdentityBase):
    pass


class OAuthUserIdentityInDBBase(OAuthUserIdentityBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class OAuthUserIdentity(OAuthUserIdentityInDBBase):
    pass


# Additional properties stored in DB
class OAuthUserIdentityInDB(OAuthUserIdentityInDBBase):
    pass

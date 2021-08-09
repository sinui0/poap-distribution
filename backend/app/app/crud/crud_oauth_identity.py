from typing import Any, Dict, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models import OAuthUserIdentity, User
from app.schemas.oauth_identity import OAuthUserIdentityCreate, OAuthUserIdentityUpdate
from app.identity.pizzly import pizzly
from app.identity import get_identity_provider


class CRUDOAuthUserIdentity(CRUDBase[OAuthUserIdentity, OAuthUserIdentityCreate, OAuthUserIdentityUpdate]):

    async def get_by_external_user_id(self, db: AsyncSession, *, provider_name: str, external_user_id: str) -> Optional[OAuthUserIdentity]:
        result = await db.execute(
            select(OAuthUserIdentity) \
            .filter(
                OAuthUserIdentity.external_user_id == external_user_id,
                OAuthUserIdentity.provider == provider_name
            )
        )
        return result.scalars().first()

    async def get_user_identities(self, db: AsyncSession, *, user: User):
        result = await db.execute(
            select(OAuthUserIdentity) \
            .filter(
                OAuthUserIdentity.user_id == user.id,
            )
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: OAuthUserIdentityCreate) -> OAuthUserIdentity:
        db_obj = OAuthUserIdentity(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: OAuthUserIdentity, obj_in: Union[OAuthUserIdentityUpdate, Dict[str, Any]]):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

oauth_identity = CRUDOAuthUserIdentity(OAuthUserIdentity)
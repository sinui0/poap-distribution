from typing import Any, Dict, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models import OAuthUserIdentity
from app.schemas.oauth_identity import OAuthUserIdentityCreate, OAuthUserIdentityUpdate


class CRUDOAuthUserIdentity(CRUDBase[OAuthUserIdentity, OAuthUserIdentityCreate, OAuthUserIdentityUpdate]):

    async def get_by_external_user_id(self, db: AsyncSession, *, external_user_id: str) -> Optional[OAuthUserIdentity]:
        result = await db.execute(select(OAuthUserIdentity).filter(OAuthUserIdentity.external_user_id == external_user_id))
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: OAuthUserIdentityCreate) -> OAuthUserIdentity:
        db_obj = OAuthUserIdentity.parse_obj(obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update():
        pass

oauth_identity = CRUDOAuthUserIdentity(CRUDOAuthUserIdentity)
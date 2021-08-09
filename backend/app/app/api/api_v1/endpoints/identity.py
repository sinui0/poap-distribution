from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[schemas.OAuthUserIdentity])
async def read_identities(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.OAuthUserIdentity = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve oauth identities.
    """
    users = await crud.oauth_identity.get_multi(db, skip=skip, limit=limit)
    return users

@router.get("/me", response_model=List[schemas.OAuthUserIdentity])
async def read_identities_me(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.OAuthUserIdentity = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve oauth identities for user.
    """
    identities = await crud.oauth_identity.get_user_identities(db, user=current_user)
    return identities


@router.post("/", response_model=schemas.OAuthUserIdentity)
async def create_identity(
    *,
    db: AsyncSession = Depends(deps.get_db),
    identity_in: schemas.OAuthUserIdentityCreate,
    current_user: models.OAuthUserIdentity = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new oauth identity.
    """
    identity = await crud.oauth_identity.get_by_external_user_id(
        db, 
        provider_name=identity_in.provider, 
        external_user_id=identity_in.external_user_id
    )
    if identity:
        raise HTTPException(
            status_code=400,
            detail="The {identity.provider} oauth identity with this external_user_id already exists in the system.",
        )
    identity = await crud.oauth_identity.create(db, obj_in=identity_in)
    return identity

@router.put("/{provider_name}/{external_user_id}", response_model=schemas.OAuthUserIdentity)
async def update_identity(
    *,
    db: AsyncSession = Depends(deps.get_db),
    provider_name: models.enums.IdentityProviderName,
    external_user_id: str,
    identity_in: schemas.OAuthUserIdentityUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an oauth identity.
    """
    identity = await crud.oauth_identity.get(db, provider_name=provider_name, external_user_id=external_user_id)
    if not identity:
        raise HTTPException(
            status_code=404,
            detail="The oauth identity with this external_user_id does not exist in the system",
        )
    identity = await crud.oauth_identity.update(db, db_obj=identity, obj_in=identity_in)
    return identity

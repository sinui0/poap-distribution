from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.identity import IdentityProviderBase, Pizzly, AuthenticationNotFound, InvalidAuthentication
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)

router = APIRouter()


@router.post("/login/access-token/", response_model=schemas.Token)
async def login_access_token(
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/access-token/external")
async def login_access_token_external(
    provider_name: models.IdentityProviderName,
    auth_id: str,
    provider: IdentityProviderBase = Depends(deps.get_provider),
    pizzly: Pizzly = Depends(deps.get_pizzly),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Using auth id for external oauth, get an access token for future requests
    """
    try:
        external_user_id = await provider.get_external_user_id(auth_id)
    except AuthenticationNotFound:
        raise HTTPException(status_code=400, detail='Provided auth id is invalid')
    except InvalidAuthentication:
        raise HTTPException(status_code=401, detail='External identity provider returned an authentication error')
    except:
        raise HTTPException(status_code=500)

    user = await crud.user.get_by_external_user_id(db, provider_name, external_user_id)
    if not user:
        raise HTTPException(status_code=500, detail='No user associated with that identity')

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.User)
async def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=schemas.Msg)
async def recover_password(email: str, db: AsyncSession = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = await crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=schemas.Msg)
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    await db.commit()
    return {"msg": "Password updated successfully"}

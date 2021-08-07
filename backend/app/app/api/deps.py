from typing import Generator
import random

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpraw import Reddit

from app import crud, models, schemas
from app.identity import Pizzly
from app.core import security
from app.core.config import settings
from app.db.session import async_session

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

reddit_client = Reddit(
    client_id=settings.REDDIT_CLIENT_ID,
    client_secret=settings.REDDIT_CLIENT_SECRET,
    redirect_uri=settings.REDDIT_REDIRECT_URL,
    user_agent='poap-distribution/0.1.0 by u/Bad_Investment'
)


async def get_db() -> Generator:
    async with async_session() as session:
        yield session

async def get_pizzly() -> Pizzly:
    yield Pizzly()

async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
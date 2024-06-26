import os
import secrets
from typing import Annotated
from fastapi import Depends, Security, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, APIKeyHeader
from app.core.database.engine import async_engine
from app.config import Config
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


async def get_async_session():
    async_session = async_sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
    )

    async with async_session.begin() as session:
        yield session


def auth_api_key(
    api_key: str = Security(APIKeyHeader(name="Authorization")),
):
    if api_key != Config.API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


# security = HTTPBasic()
#
#
# def get_current_username(
#     credentials: Annotated[HTTPBasicCredentials, Security(security)]
# ):
#     current_username_bytes = credentials.username.encode("utf8")
#     correct_username_bytes = b"stanleyjobson"
#     is_correct_username = secrets.compare_digest(
#         current_username_bytes, correct_username_bytes
#     )
#     current_password_bytes = credentials.password.encode("utf8")
#     correct_password_bytes = b"swordfish"
#     is_correct_password = secrets.compare_digest(
#         current_password_bytes, correct_password_bytes
#     )
#     if not (is_correct_username and is_correct_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return credentials.username

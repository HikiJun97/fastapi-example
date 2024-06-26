from typing import Annotated, Sequence, Any
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schemas import UserUpdate, UserCreate, UserReplace
from app.core.database.models import User
from app.dependencies import get_async_session


router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
async def get_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: Annotated[int | None, Query()] = None,
    name: Annotated[str | None, Query()] = None,
    email: Annotated[str | None, Query()] = None,
):
    select_query = select(User)
    if id is not None:
        select_query = select_query.where(User.id == id)
    if name is not None:
        select_query = select_query.where(User.name == name)
    if email is not None:
        select_query = select_query.where(User.email == email)
    if id is None and name is None and email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="There's no query parameter"
        )

    users: Sequence[User] = (await session.scalars(select_query)).all()
    return users


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    session: Annotated[AsyncSession, Depends(get_async_session)], user_data: UserCreate
):
    session.add(
        User(name=user_data.name, email=user_data.email, password=user_data.password)
    )
    return {"msg": "new user inserted"}


@router.patch("/{user_id}")
async def update_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_data: UserUpdate,
    user_id: int = Path(title="The ID of user to update"),
):
    user = (await session.scalars(select(User).where(User.id == user_id))).one()
    for key, value in user_data.model_dump(exclude_unset=True).items():
        # As this API is PATCH method, configure dictionary from BaseModel with non-default key-value pairs through "exclude_unset=True" option.
        setattr(user, key, value)
    return {"msg": "user updated"}


@router.put("/{user_id}")
async def replace_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_data: UserReplace,
    user_id: int = Path(title="The ID of user to update"),
):
    user = (await session.scalars(select(User).where(User.id == user_id))).one()
    for key, value in user_data.model_dump().items():
        setattr(user, key, value)
    return {"msg": "user replaced"}


@router.delete("/{user_id}")
async def delete_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_id: int = Path(title="The ID of user to update"),
):
    await session.execute(delete(User).where(User.id == user_id))
    return {"msg": "user deleted"}

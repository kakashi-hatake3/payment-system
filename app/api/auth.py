from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User, Admin
from app.schemas.auth import Token, LoginRequest
from app.core.security import verify_password, create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/token", response_model=Token)
async def login_for_swagger(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    """
    Универсальный эндпоинт для Swagger UI авторизации
    Проверяет сначала пользователей, затем админов
    """
    # Сначала проверяем, является ли это пользователем
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if user and verify_password(form_data.password, user.hashed_password):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_type": "user"},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    # Если не пользователь, проверяем админа
    result = await db.execute(select(Admin).where(Admin.email == form_data.username))
    admin = result.scalar_one_or_none()

    if admin and verify_password(form_data.password, admin.hashed_password):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": admin.email, "user_type": "admin"},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    # Если ни пользователь, ни админ не найдены
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

#
# @router.post("/user/login", response_model=Token)
# async def login_user(
#         login_data: LoginRequest,
#         db: AsyncSession = Depends(get_db)
# ):
#     result = await db.execute(select(User).where(User.email == login_data.email))
#     user = result.scalar_one_or_none()
#
#     if not user or not verify_password(login_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email, "user_type": "user"},
#         expires_delta=access_token_expires
#     )
#
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @router.post("/admin/login", response_model=Token)
# async def login_admin(
#         login_data: LoginRequest,
#         db: AsyncSession = Depends(get_db)
# ):
#     result = await db.execute(select(Admin).where(Admin.email == login_data.email))
#     admin = result.scalar_one_or_none()
#
#     if not admin or not verify_password(login_data.password, admin.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": admin.email, "user_type": "admin"},
#         expires_delta=access_token_expires
#     )
#
#     return {"access_token": access_token, "token_type": "bearer"}

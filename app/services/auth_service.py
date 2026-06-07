from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import user_repo
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password
from app.models.user import User

async def register_user(db: AsyncSession, user: UserCreate) -> User:
    existing_user_email = await user_repo.get_user_by_email(db, user.email)
    if existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered")
    
    existing_user_username = await user_repo.get_user_by_username(db, user.username)
    if existing_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already registered")
    
    hashed_password = hash_password(user.password)
    new_user = await user_repo.create_user(db, user,hashed_password)
    return new_user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    user = await user_repo.get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return user
    
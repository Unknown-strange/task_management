from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse,RefreshRequest
from app.services.auth_service import register_user, authenticate_user
from app.api.v1.dependencies import get_current_user
from app.models.user import User
from jose import JWTError, jwt
from app.core.config import get_settings
from app.repositories.user_repo  import  get_user_by_id

settings = get_settings()
router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data:UserCreate,db: AsyncSession=  Depends(get_db)):
    user=await register_user(db, user_data)
    return user

@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin,db:AsyncSession=Depends(get_db)):
    user = await  authenticate_user(db,login_data.email,login_data.password)
    access_token  = create_access_token(data={"sub":str(user.id)})
    refresh_token = create_refresh_token(data={"sub":str(user.id)})
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    
@router.post("/refresh",response_model=RefreshRequest)
async def  refresh_token(request: RefreshRequest,db:AsyncSession=Depends(get_db)):
    try:
        payload = jwt.decode(request.refresh_token, settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id  is None:
            raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,  detail="Invalid refresh token")
    except JWTError:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,  detail="Invalid refresh token")
    
    user = await get_user_by_id(db,user_id)
    if not user:
         raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,  detail="User not found")
     
    new_access_token = create_access_token(data={"sub": str(user.id)})
    # For simplicity, return the same refresh token; in production you'd rotate
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=request.refresh_token,
    )
    
@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: User= Depends(get_current_user)):
    return current_user
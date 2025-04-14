from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.user import User
from app.services.auth_service import get_user_by_email
from app.core.security import oauth2_scheme

router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    current_user_email = get_current_user_email(token)
    user = get_user_by_email(db, email=current_user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_user_email(token: str) -> str:
    """Helper function to decode JWT token and get user email"""
    from jose import jwt, JWTError
    from app.core.config import settings
    
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
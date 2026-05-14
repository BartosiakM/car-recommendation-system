from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, LoginResponse, UserRead
from app.utils.authentication import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_user_by_username,
    get_current_user
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return UserRead.from_orm(current_user)

@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register(user: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    """Rejestracja nowego użytkownika."""
    existing = get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Użytkownik o takiej nazwie już istnieje",
        )

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserRead.from_orm(new_user)

@router.post("/login", response_model=LoginResponse)
def login(data: UserLogin, db: Session = Depends(get_db)) -> LoginResponse:
    user = get_user_by_username(db, data.username)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowy login lub hasło",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.user_id
    )

@router.get("/test")
def test():
    return {"ok": True}

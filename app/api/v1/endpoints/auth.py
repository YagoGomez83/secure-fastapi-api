import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.user import User
from app.repositories import user_repository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["Auth"])

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def _get_current_user(
    token: str = Depends(_oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Dependency: decode JWT and return the active User or raise 401."""
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        raw_sub: str | None = payload.get("sub")
        if raw_sub is None:
            raise credentials_exc
        user_id = int(raw_sub)
    except (jwt.PyJWTError, ValueError):
        raise credentials_exc

    user = user_repository.get_by_id(db, user_id)
    if user is None or not user.is_active:
        raise credentials_exc
    return user


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> User:
    return user_service.register_user(
        db, email=payload.email, password=payload.password
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Obtain a JWT access token",
)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    token = user_service.authenticate_user(
        db, email=payload.email, password=payload.password
    )
    return TokenResponse(access_token=token)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Return the authenticated user's profile",
)
def get_me(current_user: User = Depends(_get_current_user)) -> User:
    return current_user

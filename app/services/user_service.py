from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories import user_repository


def register_user(db: Session, *, email: str, password: str) -> User:
    if user_repository.get_by_email(db, email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    hashed = hash_password(password)
    return user_repository.create(db, email=email, hashed_password=hashed)


def authenticate_user(db: Session, *, email: str, password: str) -> str:
    """Validate credentials and return a signed access token."""
    user = user_repository.get_by_email(db, email)
    # Constant-time: always run verify_password even when user is None
    # to prevent timing-based user enumeration.
    dummy_hash = "$argon2id$v=19$m=65536,t=3,p=4$placeholder"
    password_ok = verify_password(
        password, user.hashed_password if user else dummy_hash
    )

    if not user or not password_ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return create_access_token(subject=user.id)

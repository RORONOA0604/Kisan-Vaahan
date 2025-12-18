# app/core/security.py
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.core.config import settings
from jose import JWTError, jwt
from app.schemas.auth import TokenResponse
from fastapi import HTTPException, Depends, status
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from app.models.models import User
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.utils.responses import ResponseHandler

# Password hashing: prefer bcrypt_sha256 (avoids 72-byte limit),
# but keep bcrypt in schemes so old bcrypt hashes still verify.
pwd_context = CryptContext(schemes=["bcrypt_sha256", "bcrypt"], deprecated="auto")
auth_scheme = HTTPBearer()


def get_password_hash(password: str) -> str:
    """
    Hash a plaintext password. Uses bcrypt_sha256 by default.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a stored hash.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_user_token(id: int, refresh_token: Optional[str] = None) -> TokenResponse:
    """
    Returns new access & refresh tokens for a given user id.
    """
    payload = {"id": id}

    access_token_expiry = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = await create_access_token(payload, access_token_expiry)

    if not refresh_token:
        refresh_token = await create_refresh_token(payload)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=int(access_token_expiry.total_seconds())
    )


async def create_access_token(data: Dict[str, Any], access_token_expiry: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with expiry.
    """
    payload = data.copy()
    if access_token_expiry:
        expire = datetime.utcnow() + access_token_expiry
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


async def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a refresh token. By default this has no expiry or you can pass expires_delta.
    """
    payload = data.copy()
    if expires_delta:
        payload.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def get_token_payload(token: str) -> Dict[str, Any]:
    """
    Decode a JWT and return its payload or raise invalid token response.
    """
    try:
        # `algorithms` must be a list
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        # use your ResponseHandler helper to build consistent error responses
        raise ResponseHandler.invalid_token('access')


def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> int:
    """
    FastAPI dependency to extract user id from an Authorization header token.
    Returns the user id (int). If you prefer returning a User object, adjust accordingly.
    """
    payload = get_token_payload(token.credentials)
    return payload.get('id')


def check_admin_role(
        token: HTTPAuthorizationCredentials = Depends(auth_scheme),
        db: Session = Depends(get_db)
):
    """
    Dependency to require admin role. Raises 403 if not admin.
    """
    payload = get_token_payload(token.credentials)
    user_id = payload.get('id')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    role_user = db.query(User).filter(User.id == user_id).first()
    if not role_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # IMPORTANT: use the actual column name in models (user_type or role)
    # update this line if your model uses "role" instead of "user_type"
    if getattr(role_user, "user_type", None) != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")

    return role_user


def get_current_user_with_type(
        token: HTTPAuthorizationCredentials = Depends(auth_scheme),
        db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Dependency to get current user ID and type.
    Returns dict with 'user_id' and 'user_type'.
    """
    payload = get_token_payload(token.credentials)
    user_id = payload.get('id')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return {
        "user_id": user.id,
        "user_type": user.user_type
    }

from fastapi import HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.models import User
from app.db.database import get_db
from app.core.security import verify_password, get_user_token, get_token_payload
from app.core.security import get_password_hash
from app.utils.responses import ResponseHandler
from app.schemas.auth import Signup


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    @staticmethod
    async def login(user_credentials: OAuth2PasswordRequestForm, db: Session):
        user = db.query(User).filter(User.username == user_credentials.username).first()
        if not user:
            raise HTTPException(status_code=403, detail="Invalid Credentials")

        if not verify_password(user_credentials.password, user.password):
            raise HTTPException(status_code=403, detail="Invalid Credentials")

        return await get_user_token(id=user.id)

    # Login via phone (Farmer)
    @staticmethod
    async def login_with_phone(phone: str, password: str, db: Session):
        user = db.query(User).filter(User.phone == phone).first()
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=403, detail="Invalid Credentials")

        return await get_user_token(id=user.id)

    @staticmethod
    async def signup(db: Session, user: Signup):
        # Basic uniqueness checks
        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

        if user.email and db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

        if user.phone and db.query(User).filter(User.phone == user.phone).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone already exists")

        # Hash password
        hashed_password = get_password_hash(user.password)

        # build dict for model creation, avoid passing None for unique fields if you prefer
        user_data = user.model_dump()
        user_data['password'] = hashed_password

        # Ensure correct user_type
        user_type = user_data.get('user_type') or "buyer"
        if user_type not in ("buyer", "farmer", "admin"):
            user_type = "buyer"
        user_data['user_type'] = user_type

        # Create and commit
        db_user = User(**user_data)
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        return ResponseHandler.create_success("User created", db_user.id, {
            "id": db_user.id,
            "username": db_user.username,
            "user_type": db_user.user_type
        })

    @staticmethod
    async def get_refresh_token(token, db):
        payload = get_token_payload(token)
        user_id = payload.get('id', None)
        if not user_id:
            raise ResponseHandler.invalid_token('refresh')

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ResponseHandler.invalid_token('refresh')

        return await get_user_token(id=user.id, refresh_token=token)

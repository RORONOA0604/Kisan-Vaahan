from fastapi import APIRouter, Depends, status, Header ,Form
from sqlalchemy.orm import Session
from app.services.auth import AuthService
from app.db.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.schemas.auth import UserOut, Signup


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/signup", status_code=status.HTTP_200_OK)
async def signup_json(user: Signup, db: Session = Depends(get_db)):
    return await AuthService.signup(db, user)

# Accept form-encoded from HTML form (Buyer)
@router.post("/signup/buyer", status_code=status.HTTP_200_OK)
async def signup_buyer_form(
    full_name: str = Form(...),
    username: str = Form(...),
    email: str = Form(None),
    phone: str = Form(None),
    address: str = Form(None),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    signup_obj = Signup(
        full_name=full_name,
        username=username,
        email=email or None,
        phone=phone or None,
        address=address or None,
        password=password,
        user_type="buyer"
    )
    return await AuthService.signup(db, signup_obj)

# Accept form-encoded from HTML form (Farmer)
@router.post("/signup/farmer", status_code=status.HTTP_200_OK)
async def signup_farmer_form(
    full_name: str = Form(...),
    username: str = Form(...),
    phone: str = Form(...),
    location: str = Form(None),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    signup_obj = Signup(
        full_name=full_name,
        username=username,
        phone=phone or None,
        location=location or None,
        password=password,
        user_type="farmer"
    )
    return await AuthService.signup(db, signup_obj)


@router.post("/login")
async def login(
    creds: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return await AuthService.login(creds, db)


# Farmer login via phone
@router.post("/login/phone")
async def farmer_phone_login(
    phone: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    return await AuthService.login_with_phone(phone, password, db)


# Refresh token
@router.post("/refresh")
async def refresh(refresh_token: str = Form(...), db: Session = Depends(get_db)):
    return await AuthService.get_refresh_token(refresh_token, db)
from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.users import UserService
from sqlalchemy.orm import Session
from app.schemas.users import UserCreate, UserOut, UsersOut, UserOutDelete, UserUpdate
from app.core.security import check_admin_role, get_current_user


router = APIRouter(tags=["Users"], prefix="/users")


# Get Current User Profile (authenticated users)
@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_my_profile(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the profile of the currently logged-in user"""
    return UserService.get_user(db, user_id)


# Update Current User Profile (authenticated users)
@router.put("/me", status_code=status.HTTP_200_OK, response_model=UserOut)
def update_my_profile(
    updated_user: UserUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update the profile of the currently logged-in user"""
    return UserService.update_user(db, user_id, updated_user)


# Get All Users
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UsersOut,
    dependencies=[Depends(check_admin_role)])
def get_all_users(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based username"),
    role: str = Query("user", enum=["user", "admin"])
):
    return UserService.get_all_users(db, page, limit, search, role)


# Get User By ID
@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserOut,
    dependencies=[Depends(check_admin_role)])
def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_user(db, user_id)


# Create New User
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
    dependencies=[Depends(check_admin_role)])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, user)


# Update Existing User
@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserOut,
    dependencies=[Depends(check_admin_role)])
def update_user(user_id: int, updated_user: UserUpdate, db: Session = Depends(get_db)):
    return UserService.update_user(db, user_id, updated_user)


# Delete User By ID
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserOutDelete,
    dependencies=[Depends(check_admin_role)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.delete_user(db, user_id)

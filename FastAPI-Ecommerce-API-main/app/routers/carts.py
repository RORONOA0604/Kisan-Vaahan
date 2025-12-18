from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.carts import CartService
from sqlalchemy.orm import Session
from app.schemas.carts import CartCreate, CartUpdate, CartOut, CartOutDelete, CartsOutList
from app.core.security import get_current_user
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

router = APIRouter(tags=["Carts"], prefix="/carts")
auth_scheme = HTTPBearer()

@router.get("/me", status_code=status.HTTP_200_OK, response_model=CartOut)
def get_my_cart(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Return the current logged-in user's active cart (with items).
    Requires Authorization: Bearer <access_token>
    """
    return CartService.get_my_cart(db, user_id)

# Get All Carts
@router.get("/", status_code=status.HTTP_200_OK, response_model=CartsOutList)
def get_all_carts(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    return CartService.get_all_carts(token, db, page, limit)


# Get Cart By User ID
@router.get("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOut)
def get_cart(
        cart_id: int,
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return CartService.get_cart(token, db, cart_id)


# Create New Cart
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CartOut)
def create_cart(
        cart: CartCreate, db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return CartService.create_cart(token, db, cart)


# Update Existing Cart
@router.put("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOut)
def update_cart(
        cart_id: int,
        updated_cart: CartUpdate,
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return CartService.update_cart(token, db, cart_id, updated_cart)


# Delete Cart By User ID
@router.delete("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOutDelete)
def delete_cart(
        cart_id: int, db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return CartService.delete_cart(token, db, cart_id)

# POST /carts/add-item
@router.post("/add-item", status_code=status.HTTP_201_CREATED, response_model=CartOut)
def add_item_to_cart(
    payload: dict,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    payload: {"product_id": int, "quantity": int}
    Auth required (Bearer token).
    """
    return CartService.add_item(
        db=db,
        user_id=user_id,
        product_id=payload.get("product_id"),
        quantity=payload.get("quantity", 1)
    )


# PUT /carts/items/{item_id} - Update cart item quantity
@router.put("/items/{item_id}", status_code=status.HTTP_200_OK, response_model=CartOut)
def update_cart_item(
    item_id: int,
    payload: dict,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update cart item quantity.
    payload: {"quantity": int}
    """
    return CartService.update_cart_item(db, user_id, item_id, payload.get("quantity", 1))


# DELETE /carts/items/{item_id} - Remove cart item
@router.delete("/items/{item_id}", status_code=status.HTTP_200_OK, response_model=CartOut)
def remove_cart_item(
    item_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a cart item.
    """
    return CartService.remove_cart_item(db, user_id, item_id)

from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.orders import OrderService
from sqlalchemy.orm import Session
from app.schemas.orders import OrderCreate, OrderOut, OrdersOutList, OrderUpdate
from app.core.security import get_current_user, check_admin_role
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials


router = APIRouter(tags=["Orders"], prefix="/orders")
auth_scheme = HTTPBearer()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderOut)
def create_order(
    order_data: OrderCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create an order from the current user's cart.
    Requires: payment_method (COD/UPI) and delivery_address
    """
    return OrderService.create_order_from_cart(db, user_id, order_data)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=OrdersOutList)
def get_my_orders(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all orders for the logged-in user.
    """
    return OrderService.get_my_orders(db, user_id)


@router.get("/me/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderOut)
def get_my_order(
    order_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific order by ID (user can only see their own orders).
    """
    return OrderService.get_order_by_id(db, user_id, order_id)


@router.post("/me/{order_id}/cancel", status_code=status.HTTP_200_OK, response_model=OrderOut)
def cancel_my_order(
    order_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel an order (only if status is Pending).
    """
    return OrderService.cancel_order(db, user_id, order_id)


# Admin endpoints
@router.get("/", status_code=status.HTTP_200_OK, response_model=OrdersOutList, dependencies=[Depends(check_admin_role)])
def get_all_orders(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
):
    """
    Admin: Get all orders with pagination.
    """
    return OrderService.get_all_orders(db, page, limit)


@router.put("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderOut, dependencies=[Depends(check_admin_role)])
def update_order_status(
    order_id: int,
    update_data: OrderUpdate,
    db: Session = Depends(get_db)
):
    """
    Admin: Update order status (Pending, Confirmed, Delivered, Cancelled).
    """
    return OrderService.update_order_status(db, order_id, update_data)


@router.delete("/{order_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(check_admin_role)])
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Admin: Delete an order completely.
    """
    return OrderService.delete_order(db, order_id)


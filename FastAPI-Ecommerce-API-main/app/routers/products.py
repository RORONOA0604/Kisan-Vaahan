from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.products import ProductService
from sqlalchemy.orm import Session
from app.schemas.products import ProductCreate, ProductOut, ProductsOut, ProductOutDelete, ProductUpdate, ProductCreateSimple
from app.core.security import get_current_user, check_admin_role, get_current_user_with_type
from typing import List, Dict, Any


router = APIRouter(tags=["Products"], prefix="/products")


# Get All Products
@router.get("/", status_code=status.HTTP_200_OK, response_model=ProductsOut)
def get_all_products(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based title of products"),
):
    """Get all approved products (public endpoint)"""
    return ProductService.get_all_products(db, page, limit, search, include_pending=False)


# Get All Products (Admin - includes pending)
@router.get("/all", status_code=status.HTTP_200_OK, response_model=ProductsOut, dependencies=[Depends(check_admin_role)])
def get_all_products_admin(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based title of products"),
):
    """Get all products including pending (admin only)"""
    return ProductService.get_all_products(db, page, limit, search, include_pending=True)


# Get Pending Products (Admin only)
@router.get("/pending", status_code=status.HTTP_200_OK, dependencies=[Depends(check_admin_role)])
def get_pending_products(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
):
    """Get all pending products awaiting approval (admin only)"""
    return ProductService.get_pending_products(db, page, limit)


# Get Product By ID
@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return ProductService.get_product(db, product_id)


# Create New Product
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductOut)
def create_product(
        product: ProductCreate,
        user_info: Dict[str, Any] = Depends(get_current_user_with_type),
        db: Session = Depends(get_db)):
    """Create product. Farmers create pending products, admins create approved products."""
    return ProductService.create_product(
        db, 
        product, 
        user_id=user_info["user_id"], 
        user_type=user_info["user_type"]
    )


# Approve Product (Admin only)
@router.put(
    "/{product_id}/approve",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_admin_role)])
def approve_product(
        product_id: int,
        admin_user = Depends(check_admin_role),
        db: Session = Depends(get_db)):
    """Approve a pending product (admin only)"""
    return ProductService.approve_product(db, product_id, admin_user.id)


# Reject Product (Admin only)
@router.put(
    "/{product_id}/reject",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_admin_role)])
def reject_product(
        product_id: int,
        admin_user = Depends(check_admin_role),
        db: Session = Depends(get_db)):
    """Reject a pending product (admin only)"""
    return ProductService.reject_product(db, product_id, admin_user.id)


# Update Exist Product
@router.put(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductOut,
    dependencies=[Depends(check_admin_role)])
def update_product(
        product_id: int,
        updated_product: ProductUpdate,
        db: Session = Depends(get_db)):
    return ProductService.update_product(db, product_id, updated_product)


# Delete Product By ID
@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductOutDelete,
    dependencies=[Depends(check_admin_role)])
def delete_product(
        product_id: int,
        db: Session = Depends(get_db)):
    return ProductService.delete_product(db, product_id)


# Bulk Create Products
@router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductsOut)
def bulk_create_products(
        products: List[ProductCreateSimple],
        skip_duplicates: bool = Query(False, description="Skip products with duplicate titles"),
        user_id: int = Depends(get_current_user),
        db: Session = Depends(get_db)):
    """
    Bulk create products. Requires authentication (farmer or admin).
    Automatically creates categories if they don't exist.
    Set skip_duplicates=true to avoid duplicate product titles.
    """
    return ProductService.bulk_create_products(db, products, farmer_id=user_id, skip_duplicates=skip_duplicates)

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from app.schemas.products import ProductBase, CategoryBase


# Base Config
class BaseConfig:
    from_attributes = True


class ProductBaseOrder(ProductBase):
    category: CategoryBase = Field(exclude=True)

    class Config(BaseConfig):
        pass


# Order Item Schemas
class OrderItemBase(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_purchase: float
    subtotal: float
    product: ProductBaseOrder

    class Config(BaseConfig):
        pass


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


# Order Schemas
class OrderBase(BaseModel):
    id: int
    user_id: int
    total_amount: float
    payment_method: str
    delivery_address: str
    status: str
    created_at: datetime
    order_items: List[OrderItemBase]

    class Config(BaseConfig):
        pass


class OrderCreate(BaseModel):
    payment_method: str  # COD or UPI
    delivery_address: str

    class Config(BaseConfig):
        pass


class OrderOut(BaseModel):
    message: str
    data: OrderBase

    class Config(BaseConfig):
        pass


class OrdersOutList(BaseModel):
    message: str
    data: List[OrderBase]

    class Config(BaseConfig):
        pass


class OrderUpdate(BaseModel):
    status: str  # Pending, Confirmed, Delivered, Cancelled

    class Config(BaseConfig):
        pass

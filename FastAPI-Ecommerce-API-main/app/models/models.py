# app/models/models.py

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, ARRAY, Enum
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)      # Buyer uses email
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)

    phone = Column(String, unique=True, nullable=True)      # Buyer + Farmer
    address = Column(String, nullable=True)                 # Buyer delivery address
    location = Column(String, nullable=True)                # Farmer village/city

    is_active = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    # BUYER / FARMER / ADMIN
    user_type = Column(Enum("buyer", "farmer", "admin", name="user_types"),
                       nullable=False, server_default="buyer")

    # Old "role" column removed — no longer needed.

    carts = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    total_amount = Column(Float, nullable=False)

    user = relationship("User", back_populates="carts")
    cart_items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    discount_percentage = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    brand = Column(String, nullable=False)
    thumbnail = Column(String, nullable=False)
    images = Column(ARRAY(String), nullable=False)
    is_published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category = relationship("Category", back_populates="products")

    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    
    # Track which farmer uploaded this product (nullable for admin products)
    farmer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    farmer = relationship("User", foreign_keys=[farmer_id])
    
    # Product approval workflow
    approval_status = Column(Enum("pending", "approved", "rejected", name="approval_status_types"),
                            nullable=False, server_default="approved")
    approved_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    approver = relationship("User", foreign_keys=[approved_by])
    approval_date = Column(TIMESTAMP(timezone=True), nullable=True)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)  # COD or UPI
    delivery_address = Column(String, nullable=False)
    status = Column(String, nullable=False, server_default="Pending")  # Pending, Confirmed, Delivered, Cancelled
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)  # Store price at time of purchase
    subtotal = Column(Float, nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

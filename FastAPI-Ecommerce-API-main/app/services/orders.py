from sqlalchemy.orm import Session, joinedload
from app.models.models import Order, OrderItem, Cart, CartItem, Product
from app.schemas.orders import OrderCreate, OrderUpdate
from app.utils.responses import ResponseHandler
from fastapi import HTTPException, status


class OrderService:
    
    @staticmethod
    def create_order_from_cart(db: Session, user_id: int, order_data: OrderCreate):
        """
        Create an order from the user's current cart.
        """
        # Get user's active cart with items
        cart = db.query(Cart).options(
            joinedload(Cart.cart_items).joinedload(CartItem.product)
        ).filter(Cart.user_id == user_id).order_by(Cart.created_at.desc()).first()
        
        if not cart or not cart.cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty. Cannot create order."
            )
        
        # Create order
        order = Order(
            user_id=user_id,
            total_amount=cart.total_amount,
            payment_method=order_data.payment_method,
            delivery_address=order_data.delivery_address,
            status="Pending"
        )
        db.add(order)
        db.flush()  # Get order.id
        
        # Create order items from cart items
        for cart_item in cart.cart_items:
            product = cart_item.product
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price_at_purchase=float(product.price),
                subtotal=cart_item.subtotal
            )
            db.add(order_item)
        
        # Clear cart items after order creation
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        cart.total_amount = 0.0
        
        db.commit()
        db.refresh(order)
        
        # Load order with items for response
        order = db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.product)
        ).filter(Order.id == order.id).first()
        
        return ResponseHandler.create_success("Order", order.id, order)
    
    @staticmethod
    def get_my_orders(db: Session, user_id: int):
        """
        Get all orders for the logged-in user.
        """
        orders = db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.product)
        ).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()
        
        return ResponseHandler.success(f"Found {len(orders)} orders", orders)
    
    @staticmethod
    def get_order_by_id(db: Session, user_id: int, order_id: int):
        """
        Get a specific order by ID (user can only see their own orders).
        """
        order = db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.product)
        ).filter(Order.id == order_id, Order.user_id == user_id).first()
        
        if not order:
            ResponseHandler.not_found_error("Order", order_id)
        
        return ResponseHandler.get_single_success("Order", order_id, order)
    
    @staticmethod
    def get_all_orders(db: Session, page: int = 1, limit: int = 10):
        """
        Admin endpoint: Get all orders with pagination.
        """
        orders = db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.product)
        ).order_by(Order.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
        
        return ResponseHandler.success(f"Page {page} with {limit} orders", orders)
    
    @staticmethod
    def update_order_status(db: Session, order_id: int, update_data: OrderUpdate):
        """
        Admin endpoint: Update order status.
        """
        order = db.query(Order).filter(Order.id == order_id).first()
        
        if not order:
            ResponseHandler.not_found_error("Order", order_id)
        
        order.status = update_data.status
        db.commit()
        db.refresh(order)
        
        # Load with items for response
        order = db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.product)
        ).filter(Order.id == order_id).first()
        
        return ResponseHandler.update_success("Order", order_id, order)
    
    @staticmethod
    def cancel_order(db: Session, user_id: int, order_id: int):
        """
        User can cancel their own order if status is Pending.
        """
        order = db.query(Order).filter(
            Order.id == order_id,
            Order.user_id == user_id
        ).first()
        
        if not order:
            ResponseHandler.not_found_error("Order", order_id)
        
        if order.status != "Pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot cancel order with status: {order.status}"
            )
        
        order.status = "Cancelled"
        db.commit()
        db.refresh(order)
        
        # Load with items for response
        order = db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.product)
        ).filter(Order.id == order_id).first()
        
        return ResponseHandler.update_success("Order cancelled", order_id, order)
    
    @staticmethod
    def delete_order(db: Session, order_id: int):
        """
        Admin endpoint: Delete an order completely.
        """
        order = db.query(Order).filter(Order.id == order_id).first()
        
        if not order:
            ResponseHandler.not_found_error("Order", order_id)
        
        # Delete order (cascade will delete order_items)
        db.delete(order)
        db.commit()
        
        return {
            "message": f"Order {order_id} deleted successfully",
            "id": order_id
        }


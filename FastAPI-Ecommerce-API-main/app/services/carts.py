from sqlalchemy.orm import Session
from app.models.models import Cart, CartItem, Product
from app.schemas.carts import CartUpdate, CartCreate
from app.utils.responses import ResponseHandler
from sqlalchemy.orm import joinedload
from app.core.security import get_current_user


class CartService:
    
    # Get All Carts
    @staticmethod
    def get_all_carts(token, db: Session, page: int, limit: int):
        user_id = get_current_user(token)
        carts = db.query(Cart).filter(Cart.user_id == user_id).offset((page - 1) * limit).limit(limit).all()
        message = f"Page {page} with {limit} carts"
        return ResponseHandler.success(message, carts)

    # Get A Cart By ID
    @staticmethod
    def get_cart(token, db: Session, cart_id: int):
        user_id = get_current_user(token)
        cart = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == user_id).first()
        if not cart:
            ResponseHandler.not_found_error("Cart", cart_id)
        return ResponseHandler.get_single_success("cart", cart_id, cart)

    # Create a new Cart
    @staticmethod
    def create_cart(token, db: Session, cart: CartCreate):
        user_id = get_current_user(token)
        cart_dict = cart.model_dump()

        cart_items_data = cart_dict.pop("cart_items", [])
        cart_items = []
        total_amount = 0
        for item_data in cart_items_data:
            product_id = item_data['product_id']
            quantity = item_data['quantity']

            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return ResponseHandler.not_found_error("Product", product_id)

            subtotal = quantity * product.price * (product.discount_percentage / 100)
            cart_item = CartItem(product_id=product_id, quantity=quantity, subtotal=subtotal)
            total_amount += subtotal

            cart_items.append(cart_item)
        cart_db = Cart(cart_items=cart_items, user_id=user_id, total_amount=total_amount, **cart_dict)
        db.add(cart_db)
        db.commit()
        db.refresh(cart_db)
        return ResponseHandler.create_success("Cart", cart_db.id, cart_db)

    # Update Cart & CartItem
    @staticmethod
    def update_cart(token, db: Session, cart_id: int, updated_cart: CartUpdate):
        user_id = get_current_user(token)

        cart = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == user_id).first()
        if not cart:
            return ResponseHandler.not_found_error("Cart", cart_id)

        # Delete existing cart_items
        db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()

        for item in updated_cart.cart_items:
            product_id = item.product_id
            quantity = item.quantity

            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return ResponseHandler.not_found_error("Product", product_id)
            discount = product.discount_percentage or 0
            subtotal = quantity * product.price * (1 - (discount / 100))


            cart_item = CartItem(
                cart_id=cart_id,
                product_id=product_id,
                quantity=quantity,
                subtotal=subtotal
            )
            db.add(cart_item)

        cart.total_amount = sum(item.subtotal for item in cart.cart_items)

        db.commit()
        db.refresh(cart)
        return ResponseHandler.update_success("cart", cart.id, cart)

    # Delete Both Cart and CartItems
    @staticmethod
    def delete_cart(token, db: Session, cart_id: int):
        user_id = get_current_user(token)
        cart = (
            db.query(Cart)
            .options(joinedload(Cart.cart_items).joinedload(CartItem.product))
            .filter(Cart.id == cart_id, Cart.user_id == user_id)
            .first()
        )
        if not cart:
            ResponseHandler.not_found_error("Cart", cart_id)

        for cart_item in cart.cart_items:
            db.delete(cart_item)

        db.delete(cart)
        db.commit()
        return ResponseHandler.delete_success("Cart", cart_id, cart)
    @staticmethod
    def get_my_cart(db: Session, user_id: int):
        cart = db.query(Cart).options(
            joinedload(Cart.cart_items).joinedload(CartItem.product)
        ).filter(Cart.user_id == user_id).order_by(Cart.created_at.desc()).first()

        if not cart:
            cart = Cart(user_id=user_id, total_amount=0.0)
            db.add(cart)
            db.commit()
            db.refresh(cart)

        # Wrap with your existing ResponseHandler so router's response_model matches
        return ResponseHandler.create_success("cart fetched", cart.id, cart)
    @staticmethod
    def add_item(db: Session, user_id: int, product_id: int, quantity: int = 1):
        # validate inputs
        if not product_id or quantity < 1:
            raise ValueError("product_id and positive quantity required")

        # Fetch the product
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            # you can raise HTTPException instead if you want proper status code from service layer
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        # Find or create cart for user (latest active)
        cart = db.query(Cart).filter(Cart.user_id == user_id).order_by(Cart.created_at.desc()).first()
        if not cart:
            cart = Cart(user_id=user_id, total_amount=0.0)
            db.add(cart)
            db.commit()
            db.refresh(cart)

        # See if cart item for product exists, update quantity else create
        cart_item = db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        ).first()

        if cart_item:
            cart_item.quantity = cart_item.quantity + quantity
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity, subtotal=0.0)
            db.add(cart_item)

        # Compute correct subtotal for the item (apply discount safely)
        discount = getattr(product, "discount_percentage", 0) or 0
        item_price = float(product.price)
        calc_subtotal = round(cart_item.quantity * item_price * (1 - (discount / 100)), 2)
        cart_item.subtotal = calc_subtotal

        # Recalculate cart total (sum of cart_items subtotals)
        db.flush()  # push cart_item to DB session so query sees it
        items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
        total = sum(float(it.subtotal or 0) for it in items)
        cart.total_amount = round(total, 2)

        db.commit()
        db.refresh(cart)

        # Load items + product details for response
        cart = db.query(Cart).options(joinedload(Cart.cart_items).joinedload(CartItem.product)).filter(Cart.id == cart.id).first()

        return ResponseHandler.create_success("item added to cart", cart.id, cart)
    
    @staticmethod
    def update_cart_item(db: Session, user_id: int, item_id: int, quantity: int):
        """
        Update the quantity of a cart item.
        """
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        
        # Find the cart item
        cart_item = db.query(CartItem).join(Cart).filter(
            CartItem.id == item_id,
            Cart.user_id == user_id
        ).first()
        
        if not cart_item:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        
        # Update quantity
        cart_item.quantity = quantity
        
        # Recalculate subtotal
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if product:
            discount = getattr(product, "discount_percentage", 0) or 0
            item_price = float(product.price)
            cart_item.subtotal = round(quantity * item_price * (1 - (discount / 100)), 2)
        
        # Recalculate cart total
        cart = db.query(Cart).filter(Cart.id == cart_item.cart_id).first()
        items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
        total = sum(float(it.subtotal or 0) for it in items)
        cart.total_amount = round(total, 2)
        
        db.commit()
        db.refresh(cart)
        
        # Load cart with items for response
        cart = db.query(Cart).options(
            joinedload(Cart.cart_items).joinedload(CartItem.product)
        ).filter(Cart.id == cart.id).first()
        
        return ResponseHandler.update_success("cart item", item_id, cart)
    
    @staticmethod
    def remove_cart_item(db: Session, user_id: int, item_id: int):
        """
        Remove a cart item.
        """
        # Find the cart item
        cart_item = db.query(CartItem).join(Cart).filter(
            CartItem.id == item_id,
            Cart.user_id == user_id
        ).first()
        
        if not cart_item:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        
        cart_id = cart_item.cart_id
        
        # Delete the item
        db.delete(cart_item)
        db.flush()
        
        # Recalculate cart total
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
        total = sum(float(it.subtotal or 0) for it in items)
        cart.total_amount = round(total, 2)
        
        db.commit()
        db.refresh(cart)
        
        # Load cart with items for response
        cart = db.query(Cart).options(
            joinedload(Cart.cart_items).joinedload(CartItem.product)
        ).filter(Cart.id == cart.id).first()
        
        return ResponseHandler.delete_success("cart item", item_id, cart)
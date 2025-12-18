from sqlalchemy.orm import Session
from app.models.models import Product, Category, User
from app.schemas.products import ProductCreate, ProductUpdate
from app.utils.responses import ResponseHandler
from datetime import datetime
from fastapi import HTTPException, status


class ProductService:
    @staticmethod
    def get_all_products(db: Session, page: int, limit: int, search: str = "", include_pending: bool = False):
        """Get all products, filtering by approval status unless include_pending is True (admin only)"""
        query = db.query(Product).order_by(Product.id.asc()).filter(Product.title.contains(search))
        
        # Only show approved products to regular users
        if not include_pending:
            query = query.filter(Product.approval_status == "approved")
        
        products = query.limit(limit).offset((page - 1) * limit).all()
        return {"message": f"Page {page} with {limit} products", "data": products}

    @staticmethod
    def get_product(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            ResponseHandler.not_found_error("Product", product_id)
        return ResponseHandler.get_single_success(product.title, product_id, product)

    @staticmethod
    def create_product(db: Session, product: ProductCreate, user_id: int = None, user_type: str = None):
        """Create product with approval status based on user type"""
        category_exists = db.query(Category).filter(Category.id == product.category_id).first()
        if not category_exists:
            ResponseHandler.not_found_error("Category", product.category_id)

        product_dict = product.model_dump()
        
        # Set approval status based on user type
        if user_type == "farmer":
            product_dict["approval_status"] = "pending"
            product_dict["farmer_id"] = user_id
        elif user_type == "admin":
            product_dict["approval_status"] = "approved"
            product_dict["approved_by"] = user_id
            product_dict["approval_date"] = datetime.now()
        else:
            # Default to approved for backward compatibility
            product_dict["approval_status"] = "approved"
        
        db_product = Product(**product_dict)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return ResponseHandler.create_success(db_product.title, db_product.id, db_product)

    @staticmethod
    def update_product(db: Session, product_id: int, updated_product: ProductUpdate):
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            ResponseHandler.not_found_error("Product", product_id)

        for key, value in updated_product.model_dump().items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)
        return ResponseHandler.update_success(db_product.title, db_product.id, db_product)

    @staticmethod
    def delete_product(db: Session, product_id: int):
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            ResponseHandler.not_found_error("Product", product_id)
        db.delete(db_product)
        db.commit()
        return ResponseHandler.delete_success(db_product.title, db_product.id, db_product)

    @staticmethod
    def bulk_create_products(db: Session, products: list, farmer_id: int = None, skip_duplicates: bool = False):
        """
        Bulk create products with transaction safety.
        """
        from app.schemas.products import ProductCreateSimple
        
        created_products = []
        skipped_count = 0
        
        try:
            for product_data in products:
                # Check for duplicates if skip_duplicates is enabled
                if skip_duplicates:
                    existing = db.query(Product).filter(Product.title == product_data.title).first()
                    if existing:
                        skipped_count += 1
                        continue
                
                # Get or create category
                category_name = product_data.category
                category = db.query(Category).filter(Category.name == category_name).first()
                if not category:
                    category = Category(name=category_name)
                    db.add(category)
                    db.flush()  # Get category.id
                
                # Create product
                product_dict = {
                    "title": product_data.title,
                    "description": product_data.description,
                    "price": int(product_data.price),
                    "discount_percentage": product_data.discount_percentage,
                    "rating": product_data.rating,
                    "stock": product_data.stock,
                    "brand": product_data.brand,
                    "thumbnail": product_data.image,
                    "images": [product_data.image],  # Use single image for both
                    "is_published": product_data.is_published,
                    "category_id": category.id,
                    "farmer_id": farmer_id,
                    "approval_status": "pending" if farmer_id else "approved"
                }
                
                db_product = Product(**product_dict)
                db.add(db_product)
                db.flush()
                db.refresh(db_product)
                created_products.append(db_product)
            
            db.commit()
            
            message = f"Created {len(created_products)} products"
            if skipped_count > 0:
                message += f" (skipped {skipped_count} duplicates)"
            
            return {
                "message": message,
                "created": len(created_products),
                "data": created_products
            }
        
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def get_pending_products(db: Session, page: int = 1, limit: int = 50):
        """Get all pending products for admin review"""
        products = db.query(Product).filter(
            Product.approval_status == "pending"
        ).order_by(Product.created_at.desc()).limit(limit).offset((page - 1) * limit).all()
        
        total = db.query(Product).filter(Product.approval_status == "pending").count()
        
        return {
            "message": f"Found {total} pending products",
            "total": total,
            "page": page,
            "data": products
        }
    
    @staticmethod
    def approve_product(db: Session, product_id: int, admin_id: int):
        """Approve a pending product"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            ResponseHandler.not_found_error("Product", product_id)
        
        if product.approval_status == "approved":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is already approved"
            )
        
        product.approval_status = "approved"
        product.approved_by = admin_id
        product.approval_date = datetime.now()
        
        db.commit()
        db.refresh(product)
        
        return {
            "message": f"Product '{product.title}' approved successfully",
            "data": product
        }
    
    @staticmethod
    def reject_product(db: Session, product_id: int, admin_id: int):
        """Reject a pending product"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            ResponseHandler.not_found_error("Product", product_id)
        
        product.approval_status = "rejected"
        product.approved_by = admin_id
        product.approval_date = datetime.now()
        
        db.commit()
        db.refresh(product)
        
        return {
            "message": f"Product '{product.title}' rejected",
            "data": product
        }

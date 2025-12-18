"""
Quick seed script to add products directly to database without API.
Run this when you need to populate the database with initial products.
"""

from app.db.database import SessionLocal
from app.models.models import Product, Category

def seed_products():
    db = SessionLocal()
    
    try:
        # Create categories first
        categories_data = ["Vegetables", "Fruits", "Grains", "Pulses", "Millets"]
        category_map = {}
        
        for cat_name in categories_data:
            existing = db.query(Category).filter(Category.name == cat_name).first()
            if not existing:
                cat = Category(name=cat_name)
                db.add(cat)
                db.flush()
                category_map[cat_name] = cat.id
                print(f"✅ Created category: {cat_name}")
            else:
                category_map[cat_name] = existing.id
                print(f"ℹ️  Category already exists: {cat_name}")
        
        db.commit()
        
        # Sample products
        products = [
            {
                "title": "Organic Tomatoes",
                "description": "Naturally grown, juicy and full of flavor.",
                "price": 40,
                "discount_percentage": 0.0,
                "rating": 4.5,
                "stock": 120,
                "brand": "Local Farm",
                "thumbnail": "https://img.freepik.com/free-photo/top-view-ripe-fresh-tomatoes-with-water-drops-black-background_141793-3432.jpg",
                "images": ["https://img.freepik.com/free-photo/top-view-ripe-fresh-tomatoes-with-water-drops-black-background_141793-3432.jpg"],
                "category_id": category_map["Vegetables"]
            },
            {
                "title": "Green Gram",
                "description": "Rich in protein and very nutritious.",
                "price": 140,
                "discount_percentage": 0.0,
                "rating": 4.5,
                "stock": 60,
                "brand": "Local Farm",
                "thumbnail": "https://www.agrifarming.in/wp-content/uploads/Ultimate-Guide-to-Green-Gram-Farming-1.jpg",
                "images": ["https://www.agrifarming.in/wp-content/uploads/Ultimate-Guide-to-Green-Gram-Farming-1.jpg"],
                "category_id": category_map["Pulses"]
            },
            {
                "title": "Maize",
                "description": "Fresh maize perfect for flour and meals.",
                "price": 50,
                "discount_percentage": 0.0,
                "rating": 4.5,
                "stock": 200,
                "brand": "Local Farm",
                "thumbnail": "https://thumbs.dreamstime.com/b/corn-maize-seeds-close-up-shot-above-57602986.jpg",
                "images": ["https://thumbs.dreamstime.com/b/corn-maize-seeds-close-up-shot-above-57602986.jpg"],
                "category_id": category_map["Grains"]
            },
            {
                "title": "Organic Carrots",
                "description": "Sweet, crunchy carrots rich in Vitamin A.",
                "price": 40,
                "discount_percentage": 0.0,
                "rating": 4.5,
                "stock": 90,
                "brand": "Local Farm",
                "thumbnail": "https://www.tasteofhome.com/wp-content/uploads/2019/01/carrots-shutterstock_789443206.jpg",
                "images": ["https://www.tasteofhome.com/wp-content/uploads/2019/01/carrots-shutterstock_789443206.jpg"],
                "category_id": category_map["Vegetables"]
            },
            {
                "title": "Ragi",
                "description": "High in calcium & fiber. Ideal for healthy meals.",
                "price": 80,
                "discount_percentage": 0.0,
                "rating": 4.5,
                "stock": 150,
                "brand": "Local Farm",
                "thumbnail": "https://5.imimg.com/data5/SELLER/Default/2022/9/ZB/GS/FR/25008022/jiwa-organic-ragi-flour.jpg",
                "images": ["https://5.imimg.com/data5/SELLER/Default/2022/9/ZB/GS/FR/25008022/jiwa-organic-ragi-flour.jpg"],
                "category_id": category_map["Millets"]
            },
            {
                "title": "Guava",
                "description": "Fresh, crispy & naturally sweet.",
                "price": 50,
                "discount_percentage": 0.0,
                "rating": 4.5,
                "stock": 80,
                "brand": "Local Farm",
                "thumbnail": "https://growbilliontrees.com/cdn/shop/articles/guava-tree-grow-billion-trees.jpg?v=1712390096&width=1100",
                "images": ["https://growbilliontrees.com/cdn/shop/articles/guava-tree-grow-billion-trees.jpg?v=1712390096&width=1100"],
                "category_id": category_map["Fruits"]
            },
            {
                "title": "Coconuts",
                "description": "Sweet tender coconuts full of refreshing water.",
                "price": 50,
                "discount_percentage": 0.0,
                "rating": 4.5,
                "stock": 120,
                "brand": "Local Farm",
                "thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPwaITxxnnksBGzs7bVXx54f5DFKWGsZJMflRaianxpmncBI7YJzotwTuBMMCDEaoimkY&usqp=CAU",
                "images": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPwaITxxnnksBGzs7bVXx54f5DFKWGsZJMflRaianxpmncBI7YJzotwTuBMMCDEaoimkY&usqp=CAU"],
                "category_id": category_map["Fruits"]
            },
            {
                "title": "Green Capsicum",
                "description": "Crisp, fresh and perfect for curries & salads.",
                "price": 50,
                "discount_percentage": 0.0,
                "rating": 4.5,
                "stock": 100,
                "brand": "Local Farm",
                "thumbnail": "https://5.imimg.com/data5/SELLER/Default/2024/5/415703280/EK/TS/LQ/212628420/green-capsicum-500x500.webp",
                "images": ["https://5.imimg.com/data5/SELLER/Default/2024/5/415703280/EK/TS/LQ/212628420/green-capsicum-500x500.webp"],
                "category_id": category_map["Vegetables"]
            },
            {
                "title": "Nimbu",
                "description": "Fresh lemons perfect for juice, flavor & pickles.",
                "price": 50,
                "discount_percentage": 0.0,
                "rating": 4.5,
                "stock": 140,
                "brand": "Local Farm",
                "thumbnail": "https://akm-img-a-in.tosshub.com/aajtak/images/story/202303/nimbu7788778-sixteen_nine.jpg?size=948:533",
                "images": ["https://akm-img-a-in.tosshub.com/aajtak/images/story/202303/nimbu7788778-sixteen_nine.jpg?size=948:533"],
                "category_id": category_map["Fruits"]
            }
        ]
        
        # Add products
        created_count = 0
        for p_data in products:
            existing = db.query(Product).filter(Product.title == p_data["title"]).first()
            if not existing:
                product = Product(**p_data)
                db.add(product)
                created_count += 1
                print(f"✅ Created product: {p_data['title']}")
            else:
                print(f"ℹ️  Product already exists: {p_data['title']}")
        
        db.commit()
        print(f"\n🎉 Successfully seeded {created_count} products!")
        print(f"📊 Total products in database: {db.query(Product).count()}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding products into database...\n")
    seed_products()

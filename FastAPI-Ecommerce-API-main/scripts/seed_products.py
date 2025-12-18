#!/usr/bin/env python3
"""
Seed products into the Kisan Vaahan database via the bulk API endpoint.

Usage:
    python scripts/seed_products.py --token YOUR_ACCESS_TOKEN
    
Or set the token as an environment variable:
    export KISAN_AUTH_TOKEN=your_token_here
    python scripts/seed_products.py
"""

import requests
import sys
import os
import argparse
import json


# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
BULK_ENDPOINT = f"{API_BASE_URL}/products/bulk"

# Product data to seed
SEED_PRODUCTS = [
    {
        "title": "Organic Tomatoes",
        "category": "Vegetables",
        "price": 40,
        "image": "https://img.freepik.com/free-photo/top-view-ripe-fresh-tomatoes-with-water-drops-black-background_141793-3432.jpg",
        "description": "Naturally grown, juicy and full of flavor.",
        "stock": 120
    },
    {
        "title": "Green Gram",
        "category": "Pulses",
        "price": 140,
        "image": "https://www.agrifarming.in/wp-content/uploads/Ultimate-Guide-to-Green-Gram-Farming-1.jpg",
        "description": "Rich in protein and very nutritious.",
        "stock": 60
    },
    {
        "title": "Maize",
        "category": "Grains",
        "price": 50,
        "image": "https://thumbs.dreamstime.com/b/corn-maize-seeds-close-up-shot-above-57602986.jpg",
        "description": "Fresh maize perfect for flour and meals.",
        "stock": 200
    },
    {
        "title": "Organic Carrots",
        "category": "Vegetables",
        "price": 40,
        "image": "https://www.tasteofhome.com/wp-content/uploads/2019/01/carrots-shutterstock_789443206.jpg",
        "description": "Sweet, crunchy carrots rich in Vitamin A.",
        "stock": 90
    },
    {
        "title": "Ragi",
        "category": "Millets",
        "price": 80,
        "image": "https://5.imimg.com/data5/SELLER/Default/2022/9/ZB/GS/FR/25008022/jiwa-organic-ragi-flour.jpg",
        "description": "High in calcium & fiber. Ideal for healthy meals.",
        "stock": 150
    },
    {
        "title": "Guava",
        "category": "Fruits",
        "price": 50,
        "image": "https://growbilliontrees.com/cdn/shop/articles/guava-tree-grow-billion-trees.jpg?v=1712390096&width=1100",
        "description": "Fresh, crispy & naturally sweet.",
        "stock": 80
    },
    {
        "title": "Coconuts",
        "category": "Fruits",
        "price": 50,
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPwaITxxnnksBGzs7bVXx54f5DFKWGsZJMflRaianxpmncBI7YJzotwTuBMMCDEaoimkY&usqp=CAU",
        "description": "Sweet tender coconuts full of refreshing water.",
        "stock": 120
    },
    {
        "title": "Green Capsicum",
        "category": "Vegetables",
        "price": 50,
        "image": "https://5.imimg.com/data5/SELLER/Default/2024/5/415703280/EK/TS/LQ/212628420/green-capsicum-500x500.webp",
        "description": "Crisp, fresh and perfect for curries & salads.",
        "stock": 100
    },
    {
        "title": "Nimbu",
        "category": "Fruits",
        "price": 50,
        "image": "https://akm-img-a-in.tosshub.com/aajtak/images/story/202303/nimbu7788778-sixteen_nine.jpg?size=948:533",
        "description": "Fresh lemons perfect for juice, flavor & pickles.",
        "stock": 140
    }
]


def seed_products(token: str, skip_duplicates: bool = True):
    """
    Seed products via the bulk API endpoint.
    
    Args:
        token: JWT access token for authentication
        skip_duplicates: If True, skip products with duplicate titles
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    params = {"skip_duplicates": skip_duplicates}
    
    print(f"🌱 Seeding {len(SEED_PRODUCTS)} products to {BULK_ENDPOINT}...")
    print(f"   Skip duplicates: {skip_duplicates}")
    
    try:
        response = requests.post(
            BULK_ENDPOINT,
            headers=headers,
            params=params,
            json=SEED_PRODUCTS,
            timeout=30
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"\n✅ Success! {data.get('message', 'Products created')}")
            print(f"   Created: {data.get('created', 0)} products")
            
            if data.get('data'):
                print("\n📦 Created products:")
                for product in data['data']:
                    print(f"   - {product['title']} (ID: {product['id']}, Stock: {product['stock']})")
            
            return True
        
        elif response.status_code == 401:
            print("\n❌ Authentication failed. Please check your token.")
            print("   Make sure you're using a valid farmer or admin token.")
            return False
        
        elif response.status_code == 422:
            print("\n❌ Validation error:")
            print(json.dumps(response.json(), indent=2))
            return False
        
        else:
            print(f"\n❌ Error: HTTP {response.status_code}")
            print(response.text)
            return False
    
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Connection error. Is the server running at {API_BASE_URL}?")
        return False
    
    except requests.exceptions.Timeout:
        print("\n❌ Request timed out. Server might be slow or unresponsive.")
        return False
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False


def main():
    global API_BASE_URL, BULK_ENDPOINT
    
    parser = argparse.ArgumentParser(description="Seed products into Kisan Vaahan database")
    parser.add_argument(
        "--token",
        help="JWT access token (or set KISAN_AUTH_TOKEN env var)",
        default=os.getenv("KISAN_AUTH_TOKEN")
    )
    parser.add_argument(
        "--no-skip-duplicates",
        action="store_true",
        help="Don't skip duplicate products (will fail if duplicates exist)"
    )
    parser.add_argument(
        "--api-url",
        help="API base URL",
        default=API_BASE_URL
    )
    
    args = parser.parse_args()
    
    if not args.token:
        print("❌ Error: No authentication token provided.")
        print("\nPlease provide a token using one of these methods:")
        print("  1. Command line: python seed_products.py --token YOUR_TOKEN")
        print("  2. Environment variable: export KISAN_AUTH_TOKEN=YOUR_TOKEN")
        print("\nTo get a token:")
        print("  1. Login as a farmer or admin user")
        print("  2. Use the access_token from the login response")
        sys.exit(1)
    
    # Update API URL if provided
    if args.api_url != API_BASE_URL:
        API_BASE_URL = args.api_url
        BULK_ENDPOINT = f"{API_BASE_URL}/products/bulk"
    
    skip_duplicates = not args.no_skip_duplicates
    success = seed_products(args.token, skip_duplicates)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

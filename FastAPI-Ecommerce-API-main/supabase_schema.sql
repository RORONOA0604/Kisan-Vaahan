-- Kisan Vaahan Database Schema for Supabase
-- Execute this SQL in your Supabase SQL Editor

-- Enable UUID extension (optional, for future use)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create ENUM types
CREATE TYPE user_types AS ENUM ('buyer', 'farmer', 'admin');
CREATE TYPE approval_status_types AS ENUM ('pending', 'approved', 'rejected');

-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50) UNIQUE,
    address TEXT,
    location VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    user_type user_types DEFAULT 'buyer' NOT NULL
);

-- Categories Table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Products Table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL,
    discount_percentage FLOAT DEFAULT 0 NOT NULL,
    rating FLOAT DEFAULT 0 NOT NULL,
    stock INTEGER DEFAULT 0 NOT NULL,
    brand VARCHAR(255) NOT NULL,
    thumbnail TEXT NOT NULL,
    images TEXT[] NOT NULL,
    is_published BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    farmer_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    approval_status approval_status_types DEFAULT 'approved' NOT NULL,
    approved_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    approval_date TIMESTAMP WITH TIME ZONE
);

-- Carts Table
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    total_amount FLOAT NOT NULL
);

-- Cart Items Table
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    subtotal FLOAT NOT NULL
);

-- Orders Table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    total_amount FLOAT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    delivery_address TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Order Items Table
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    price_at_purchase FLOAT NOT NULL,
    subtotal FLOAT NOT NULL
);

-- Create Indexes for Performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_user_type ON users(user_type);

CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_farmer_id ON products(farmer_id);
CREATE INDEX idx_products_approval_status ON products(approval_status);
CREATE INDEX idx_products_is_published ON products(is_published);

CREATE INDEX idx_carts_user_id ON carts(user_id);
CREATE INDEX idx_cart_items_cart_id ON cart_items(cart_id);
CREATE INDEX idx_cart_items_product_id ON cart_items(product_id);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Insert Default Categories
INSERT INTO categories (name) VALUES 
    ('Vegetables'),
    ('Fruits'),
    ('Grains'),
    ('Pulses'),
    ('Millets'),
    ('Dairy'),
    ('Spices'),
    ('Others');

-- Insert Default Admin User
-- Password: admin123 (hashed with bcrypt)
-- IMPORTANT: Change this password after first login!
INSERT INTO users (username, email, password, full_name, user_type, is_active) VALUES 
    ('admin', 'admin@kisanvaahan.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5aeUXL.dEh4Oi', 'System Administrator', 'admin', TRUE);

-- Insert Sample Products (All Approved)
INSERT INTO products (title, description, price, discount_percentage, rating, stock, brand, thumbnail, images, category_id, approval_status) VALUES
    ('Organic Tomatoes', 'Naturally grown, juicy and full of flavor.', 40, 0, 4.5, 100, 'Farmer Direct', 'https://img.freepik.com/free-photo/top-view-ripe-fresh-tomatoes-with-water-drops-black-background_141793-3432.jpg', ARRAY['https://img.freepik.com/free-photo/top-view-ripe-fresh-tomatoes-with-water-drops-black-background_141793-3432.jpg'], 1, 'approved'),
    ('Green Gram', 'Rich in protein and very nutritious.', 140, 0, 4.7, 50, 'Organic Farm', 'https://www.agrifarming.in/wp-content/uploads/Ultimate-Guide-to-Green-Gram-Farming-1.jpg', ARRAY['https://www.agrifarming.in/wp-content/uploads/Ultimate-Guide-to-Green-Gram-Farming-1.jpg'], 4, 'approved'),
    ('Maize', 'Fresh maize perfect for flour and meals.', 50, 0, 4.3, 80, 'Farm Fresh', 'https://thumbs.dreamstime.com/b/corn-maize-seeds-close-up-shot-above-57602986.jpg', ARRAY['https://thumbs.dreamstime.com/b/corn-maize-seeds-close-up-shot-above-57602986.jpg'], 3, 'approved'),
    ('Organic Carrots', 'Sweet, crunchy carrots rich in Vitamin A.', 40, 0, 4.6, 120, 'Farmer Direct', 'https://www.tasteofhome.com/wp-content/uploads/2019/01/carrots-shutterstock_789443206.jpg', ARRAY['https://www.tasteofhome.com/wp-content/uploads/2019/01/carrots-shutterstock_789443206.jpg'], 1, 'approved'),
    ('Ragi', 'High in calcium & fiber. Ideal for healthy meals.', 80, 0, 4.8, 60, 'Millet Farm', 'https://5.imimg.com/data5/SELLER/Default/2022/9/ZB/GS/FR/25008022/jiwa-organic-ragi-flour.jpg', ARRAY['https://5.imimg.com/data5/SELLER/Default/2022/9/ZB/GS/FR/25008022/jiwa-organic-ragi-flour.jpg'], 5, 'approved'),
    ('Guava', 'Fresh, crispy & naturally sweet.', 50, 0, 4.4, 90, 'Fruit Garden', 'https://growbilliontrees.com/cdn/shop/articles/guava-tree-grow-billion-trees.jpg?v=1712390096&width=1100', ARRAY['https://growbilliontrees.com/cdn/shop/articles/guava-tree-grow-billion-trees.jpg?v=1712390096&width=1100'], 2, 'approved'),
    ('Coconuts', 'Sweet tender coconuts full of refreshing water.', 50, 0, 4.5, 70, 'Coastal Farm', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPwaITxxnnksBGzs7bVXx54f5DFKWGsZJMflRaianxpmncBI7YJzotwTuBMMCDEaoimkY&usqp=CAU', ARRAY['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPwaITxxnnksBGzs7bVXx54f5DFKWGsZJMflRaianxpmncBI7YJzotwTuBMMCDEaoimkY&usqp=CAU'], 2, 'approved'),
    ('Green Capsicum', 'Crisp, fresh and perfect for curries & salads.', 50, 0, 4.2, 110, 'Veggie Farm', 'https://5.imimg.com/data5/SELLER/Default/2024/5/415703280/EK/TS/LQ/212628420/green-capsicum-500x500.webp', ARRAY['https://5.imimg.com/data5/SELLER/Default/2024/5/415703280/EK/TS/LQ/212628420/green-capsicum-500x500.webp'], 1, 'approved'),
    ('Nimbu', 'Fresh lemons perfect for juice, flavor & pickles.', 50, 0, 4.3, 100, 'Citrus Farm', 'https://akm-img-a-in.tosshub.com/aajtak/images/story/202303/nimbu7788778-sixteen_nine.jpg?size=948:533', ARRAY['https://akm-img-a-in.tosshub.com/aajtak/images/story/202303/nimbu7788778-sixteen_nine.jpg?size=948:533'], 2, 'approved');

-- Grant necessary permissions (Supabase handles this automatically, but included for reference)
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE products ENABLE ROW LEVEL SECURITY;
-- etc.

-- Success message
SELECT 'Database schema created successfully!' AS message;

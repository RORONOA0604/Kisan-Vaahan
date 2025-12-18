-- Manual migration to add missing columns
-- Run this SQL script to update your database schema

-- Add farmer_id column to products table
ALTER TABLE products 
ADD COLUMN IF NOT EXISTS farmer_id INTEGER;

-- Add foreign key constraint
ALTER TABLE products 
ADD CONSTRAINT fk_products_farmer_id 
FOREIGN KEY (farmer_id) REFERENCES users(id) ON DELETE SET NULL;

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    total_amount FLOAT NOT NULL,
    payment_method VARCHAR NOT NULL,
    delivery_address TEXT NOT NULL,
    status VARCHAR NOT NULL DEFAULT 'Pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price_at_purchase FLOAT NOT NULL,
    subtotal FLOAT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Verify the changes
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'products' 
ORDER BY ordinal_position;

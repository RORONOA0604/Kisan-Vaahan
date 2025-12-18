-- Seed Products SQL Script
-- This script inserts the initial 9 products into the database
-- Prerequisites:
--   1. Categories table must exist
--   2. A farmer user with id=1 must exist (or adjust farmer_id below)

-- First, ensure categories exist
INSERT INTO categories (name) VALUES ('Vegetables') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name) VALUES ('Pulses') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name) VALUES ('Grains') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name) VALUES ('Millets') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name) VALUES ('Fruits') ON CONFLICT (name) DO NOTHING;

-- Get category IDs (PostgreSQL specific)
DO $$
DECLARE
    cat_vegetables_id INT;
    cat_pulses_id INT;
    cat_grains_id INT;
    cat_millets_id INT;
    cat_fruits_id INT;
BEGIN
    SELECT id INTO cat_vegetables_id FROM categories WHERE name = 'Vegetables';
    SELECT id INTO cat_pulses_id FROM categories WHERE name = 'Pulses';
    SELECT id INTO cat_grains_id FROM categories WHERE name = 'Grains';
    SELECT id INTO cat_millets_id FROM categories WHERE name = 'Millets';
    SELECT id INTO cat_fruits_id FROM categories WHERE name = 'Fruits';

    -- Insert products (using farmer_id = 1, adjust if needed)
    -- Product 1: Organic Tomatoes
    INSERT INTO products (
        title, description, price, discount_percentage, rating, stock, brand, 
        thumbnail, images, is_published, category_id, farmer_id
    ) VALUES (
        'Organic Tomatoes',
        'Naturally grown, juicy and full of flavor.',
        40,
        0.0,
        4.5,
        120,
        'Local Farm',
        'https://img.freepik.com/free-photo/top-view-ripe-fresh-tomatoes-with-water-drops-black-background_141793-3432.jpg',
        ARRAY['https://img.freepik.com/free-photo/top-view-ripe-fresh-tomatoes-with-water-drops-black-background_141793-3432.jpg'],
        TRUE,
        cat_vegetables_id,
        1
    ) ON CONFLICT (title) DO NOTHING;

    -- Product 2: Green Gram
    INSERT INTO products (
        title, description, price, discount_percentage, rating, stock, brand, 
        thumbnail, images, is_published, category_id, farmer_id
    ) VALUES (
        'Green Gram',
        'Rich in protein and very nutritious.',
        140,
        0.0,
        4.5,
        60,
        'Local Farm',
        'https://www.agrifarming.in/wp-content/uploads/Ultimate-Guide-to-Green-Gram-Farming-1.jpg',
        ARRAY['https://www.agrifarming.in/wp-content/uploads/Ultimate-Guide-to-Green-Gram-Farming-1.jpg'],
        TRUE,
        cat_pulses_id,
        1
    ) ON CONFLICT (title) DO NOTHING;

    -- Product 3: Maize
    INSERT INTO products (
        title, description, price, discount_percentage, rating, stock, brand, 
        thumbnail, images, is_published, category_id, farmer_id
    ) VALUES (
        'Maize',
        'Fresh maize perfect for flour and meals.',
        50,
        0.0,
        4.5,
        200,
        'Local Farm',
        'https://thumbs.dreamstime.com/b/corn-maize-seeds-close-up-shot-above-57602986.jpg',
        ARRAY['https://thumbs.dreamstime.com/b/corn-maize-seeds-close-up-shot-above-57602986.jpg'],
        TRUE,
        cat_grains_id,
        1
    ) ON CONFLICT (title) DO NOTHING;

    -- Product 4: Organic Carrots
    INSERT INTO products (
        title, description, price, discount_percentage, rating, stock, brand, 
        thumbnail, images, is_published, category_id, farmer_id
    ) VALUES (
        'Organic Carrots',
        'Sweet, crunchy carrots rich in Vitamin A.',
        40,
        0.0,
        4.5,
        90,
        'Local Farm',
        'https://www.tasteofhome.com/wp-content/uploads/2019/01/carrots-shutterstock_789443206.jpg',
        ARRAY['https://www.tasteofhome.com/wp-content/uploads/2019/01/carrots-shutterstock_789443206.jpg'],
        TRUE,
        cat_vegetables_id,
        1
    ) ON CONFLICT (title) DO NOTHING;

    -- Product 5: Ragi
    INSERT INTO products (
        title, description, price, discount_percentage, rating, stock, brand, 
        thumbnail, images, is_published, category_id, farmer_id
    ) VALUES (
        'Ragi',
        'High in calcium & fiber. Ideal for healthy meals.',
        80,
        0.0,
        4.5,
        150,
        'Local Farm',
        'https://5.imimg.com/data5/SELLER/Default/2022/9/ZB/GS/FR/25008022/jiwa-organic-ragi-flour.jpg',
        ARRAY['https://5.imimg.com/data5/SELLER/Default/2022/9/ZB/GS/FR/25008022/jiwa-organic-ragi-flour.jpg'],
        TRUE,
        cat_millets_id,
        1
    ) ON CONFLICT (title) DO NOTHING;

    -- Product 6: Guava
    INSERT INTO products (
        title, description, price, discount_percentage, rating, stock, brand, 
        thumbnail, images, is_published, category_id, farmer_id
    ) VALUES (
        'Guava',
        'Fresh, crispy & naturally sweet.',
        50,
        0.0,
        4.5,
        80,
        'Local Farm',
        'https://growbilliontrees.com/cdn/shop/articles/guava-tree-grow-billion-trees.jpg?v=1712390096&width=1100',
        ARRAY['https://growbilliontrees.com/cdn/shop/articles/guava-tree-grow-billion-trees.jpg?v=1712390096&width=1100'],
        TRUE,
        cat_fruits_id,
        1
    ) ON CONFLICT (title) DO NOTHING;

    -- Product 7: Coconuts
    INSERT INTO products (
        title, description, price, discount_percentage, rating, stock, brand, 
        thumbnail, images, is_published, category_id, farmer_id
    ) VALUES (
        'Coconuts',
        'Sweet tender coconuts full of refreshing water.',
        50,
        0.0,
        4.5,
        120,
        'Local Farm',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPwaITxxnnksBGzs7bVXx54f5DFKWGsZJMflRaianxpmncBI7YJzotwTuBMMCDEaoimkY&usqp=CAU',
        ARRAY['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPwaITxxnnksBGzs7bVXx54f5DFKWGsZJMflRaianxpmncBI7YJzotwTuBMMCDEaoimkY&usqp=CAU'],
        TRUE,
        cat_fruits_id,
        1
    ) ON CONFLICT (title) DO NOTHING;

    -- Product 8: Green Capsicum
    INSERT INTO products (
        title, description, price, discount_percentage, rating, stock, brand, 
        thumbnail, images, is_published, category_id, farmer_id
    ) VALUES (
        'Green Capsicum',
        'Crisp, fresh and perfect for curries & salads.',
        50,
        0.0,
        4.5,
        100,
        'Local Farm',
        'https://5.imimg.com/data5/SELLER/Default/2024/5/415703280/EK/TS/LQ/212628420/green-capsicum-500x500.webp',
        ARRAY['https://5.imimg.com/data5/SELLER/Default/2024/5/415703280/EK/TS/LQ/212628420/green-capsicum-500x500.webp'],
        TRUE,
        cat_vegetables_id,
        1
    ) ON CONFLICT (title) DO NOTHING;

    -- Product 9: Nimbu
    INSERT INTO products (
        title, description, price, discount_percentage, rating, stock, brand, 
        thumbnail, images, is_published, category_id, farmer_id
    ) VALUES (
        'Nimbu',
        'Fresh lemons perfect for juice, flavor & pickles.',
        50,
        0.0,
        4.5,
        140,
        'Local Farm',
        'https://akm-img-a-in.tosshub.com/aajtak/images/story/202303/nimbu7788778-sixteen_nine.jpg?size=948:533',
        ARRAY['https://akm-img-a-in.tosshub.com/aajtak/images/story/202303/nimbu7788778-sixteen_nine.jpg?size=948:533'],
        TRUE,
        cat_fruits_id,
        1
    ) ON CONFLICT (title) DO NOTHING;

END $$;

-- Verify the inserts
SELECT COUNT(*) as total_products FROM products;
SELECT c.name as category, COUNT(p.id) as product_count 
FROM categories c 
LEFT JOIN products p ON c.id = p.category_id 
GROUP BY c.name 
ORDER BY c.name;

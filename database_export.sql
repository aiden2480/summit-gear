BEGIN TRANSACTION;
CREATE TABLE cart_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            );
CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                image_url TEXT NOT NULL,
                category TEXT NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0
            );
INSERT INTO "products" VALUES(1,'Wireless Bluetooth Headphones','Premium noise-cancelling wireless headphones with 30-hour battery life and comfortable over-ear design.',89.99,'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop','Electronics',25);
INSERT INTO "products" VALUES(2,'Organic Cotton T-Shirt','Soft and breathable 100% organic cotton t-shirt available in multiple colours. Ethically sourced.',29.99,'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop','Clothing',50);
INSERT INTO "products" VALUES(3,'Stainless Steel Water Bottle','Double-wall insulated 750ml water bottle. Keeps drinks cold for 24 hours or hot for 12 hours.',24.95,'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=400&fit=crop','Home & Kitchen',40);
INSERT INTO "products" VALUES(4,'Mechanical Keyboard','RGB backlit mechanical keyboard with Cherry MX Blue switches and aluminium frame.',119.0,'https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=400&h=400&fit=crop','Electronics',15);
INSERT INTO "products" VALUES(5,'Running Shoes','Lightweight and responsive running shoes with cushioned sole and breathable mesh upper.',74.5,'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop','Clothing',30);
INSERT INTO "products" VALUES(6,'Ceramic Coffee Mug Set','Set of 4 handcrafted ceramic coffee mugs in earthy tones. Microwave and dishwasher safe.',34.99,'https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400&h=400&fit=crop','Home & Kitchen',20);
INSERT INTO "products" VALUES(7,'Portable Power Bank','20000mAh portable charger with fast charging support and dual USB-C ports.',45.0,'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=400&h=400&fit=crop','Electronics',35);
INSERT INTO "products" VALUES(8,'Yoga Mat','Non-slip eco-friendly yoga mat with alignment lines. 6mm thick for extra comfort.',39.99,'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=400&fit=crop','Sports',22);
INSERT INTO "products" VALUES(9,'LED Desk Lamp','Adjustable LED desk lamp with 5 brightness levels, 3 colour temperatures, and USB charging port.',42.0,'https://images.unsplash.com/photo-1507473885765-e6ed057ab6fe?w=400&h=400&fit=crop','Home & Kitchen',18);
INSERT INTO "products" VALUES(10,'Canvas Backpack','Durable canvas backpack with padded laptop compartment and water-resistant coating.',54.99,'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop','Accessories',28);
INSERT INTO "products" VALUES(11,'Wireless Mouse','Ergonomic wireless mouse with silent click and adjustable DPI up to 4000.',27.5,'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop','Electronics',45);
INSERT INTO "products" VALUES(12,'Scented Candle Set','Luxury soy wax candle set with lavender, vanilla, and eucalyptus fragrances. 40-hour burn time each.',32.0,'https://images.unsplash.com/photo-1602607861047-0914a83498b3?w=400&h=400&fit=crop','Home & Kitchen',33);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('products',12);
INSERT INTO "sqlite_sequence" VALUES('cart_items',1);
COMMIT;

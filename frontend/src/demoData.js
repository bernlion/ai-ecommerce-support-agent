export const demoProducts = [
  { product_id: 'P1001', name: 'Samsung Galaxy S24', description: 'Flagship Android phone with AMOLED display and AI camera tools.', price: 58999, brand: 'Samsung', category: 'Smartphones', stock: 18, rating: 4.6 },
  { product_id: 'P1002', name: 'Apple iPhone 15', description: 'A16-powered iPhone with Dynamic Island and excellent camera quality.', price: 69900, brand: 'Apple', category: 'Smartphones', stock: 9, rating: 4.7 },
  { product_id: 'P1003', name: 'OnePlus Nord CE 4', description: 'Fast mid-range smartphone with long battery life.', price: 24999, brand: 'OnePlus', category: 'Smartphones', stock: 32, rating: 4.3 },
  { product_id: 'P1004', name: 'Lenovo IdeaPad Slim 5', description: 'Everyday laptop with Ryzen 7, 16GB RAM, and 512GB SSD.', price: 57990, brand: 'Lenovo', category: 'Laptops', stock: 13, rating: 4.4 },
  { product_id: 'P1005', name: 'ASUS TUF Gaming F15', description: 'Gaming laptop with Intel i5, RTX graphics, and 144Hz display.', price: 71990, brand: 'ASUS', category: 'Laptops', stock: 7, rating: 4.5 },
  { product_id: 'P1006', name: 'HP 15s Student Laptop', description: 'Lightweight laptop for students with Intel i5 and full HD display.', price: 52999, brand: 'HP', category: 'Laptops', stock: 16, rating: 4.2 },
  { product_id: 'P1007', name: 'Sony WH-CH720N', description: 'Wireless noise-cancelling headphones with up to 35 hours battery.', price: 8990, brand: 'Sony', category: 'Headphones', stock: 25, rating: 4.4 },
  { product_id: 'P1008', name: 'boAt Rockerz 450', description: 'Affordable wireless headphones with punchy bass.', price: 1499, brand: 'boAt', category: 'Headphones', stock: 60, rating: 4.0 },
  { product_id: 'P1009', name: 'Samsung Galaxy Watch6', description: 'Smart watch with health tracking and Wear OS apps.', price: 22999, brand: 'Samsung', category: 'Smart Watches', stock: 11, rating: 4.5 },
  { product_id: 'P1010', name: 'Apple iPad 10th Gen', description: '10.9-inch tablet for study, entertainment, and creative work.', price: 34900, brand: 'Apple', category: 'Tablets', stock: 14, rating: 4.6 },
  { product_id: 'P1011', name: 'Samsung Galaxy Tab S9 FE', description: 'Android tablet with S Pen support and vivid display.', price: 32999, brand: 'Samsung', category: 'Tablets', stock: 10, rating: 4.4 },
  { product_id: 'P1012', name: 'Logitech Pebble Mouse 2', description: 'Compact Bluetooth mouse for laptops and tablets.', price: 2295, brand: 'Logitech', category: 'Accessories', stock: 45, rating: 4.3 },
];

export const demoOrders = [
  { order_id: 'ORD1001', customer_id: 'C1001', products: ['P1004'], status: 'Shipped', expected_delivery: '2026-09-08' },
  { order_id: 'ORD1002', customer_id: 'C1001', products: ['P1007', 'P1012'], status: 'Processing', expected_delivery: '2026-09-10' },
  { order_id: 'ORD1003', customer_id: 'C1001', products: ['P1009'], status: 'Delivered', expected_delivery: '2026-09-01' },
];

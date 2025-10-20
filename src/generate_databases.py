"""
Transactional Database Generator
Generates 5 deterministic transactional databases for different retailers
"""

import csv
import hashlib

# Define items for each store
STORE_ITEMS = {
    'Amazon': [
        'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 
        'USB_Cable', 'Webcam', 'External_HDD', 'Phone_Charger', 
        'HDMI_Cable', 'Router', 'RAM', 'SSD', 'Graphics_Card', 'Microphone'
    ],
    'BestBuy': [
        'TV', 'Soundbar', 'Gaming_Console', 'Controller', 'Smart_Watch',
        'Tablet', 'Earbuds', 'Phone_Case', 'Screen_Protector', 'Power_Bank',
        'Bluetooth_Speaker', 'Drone', 'Camera', 'Tripod', 'Memory_Card'
    ],
    'Walmart': [
        'Milk', 'Bread', 'Eggs', 'Butter', 'Cheese', 'Cereal', 'Coffee',
        'Tea', 'Sugar', 'Flour', 'Rice', 'Pasta', 'Tomato_Sauce', 
        'Olive_Oil', 'Salt', 'Pepper', 'Chicken', 'Beef'
    ],
    'Target': [
        'T_Shirt', 'Jeans', 'Sneakers', 'Socks', 'Jacket', 'Hat',
        'Backpack', 'Sunglasses', 'Watch', 'Belt', 'Wallet', 'Scarf',
        'Gloves', 'Sweater', 'Dress'
    ],
    'Costco': [
        'Paper_Towels', 'Toilet_Paper', 'Detergent', 'Dish_Soap', 
        'Shampoo', 'Toothpaste', 'Trash_Bags', 'Batteries', 
        'Light_Bulbs', 'Water_Bottles', 'Snacks_Box', 'Frozen_Pizza',
        'Rotisserie_Chicken', 'Muffins', 'Nuts_Pack'
    ]
}

# Define deterministic transaction patterns based on common shopping behaviors
def generate_deterministic_transactions(store_name, items, num_transactions=25):
    """Generate deterministic transactions using hash-based selection"""
    transactions = []
    
    # Define common item combinations for each store
    patterns = {
        'Amazon': [
            ['Laptop', 'Mouse', 'Keyboard'],
            ['Monitor', 'HDMI_Cable'],
            ['Headphones', 'USB_Cable'],
            ['External_HDD', 'USB_Cable'],
            ['Router', 'HDMI_Cable'],
            ['Laptop', 'Mouse', 'Keyboard', 'Monitor'],
            ['RAM', 'SSD'],
            ['Graphics_Card', 'Monitor'],
            ['Webcam', 'Microphone', 'Headphones'],
            ['Phone_Charger', 'USB_Cable'],
        ],
        'BestBuy': [
            ['TV', 'Soundbar', 'HDMI_Cable'],
            ['Gaming_Console', 'Controller', 'TV'],
            ['Smart_Watch', 'Phone_Case'],
            ['Tablet', 'Screen_Protector', 'Phone_Case'],
            ['Earbuds', 'Phone_Case'],
            ['Camera', 'Tripod', 'Memory_Card'],
            ['Bluetooth_Speaker', 'Power_Bank'],
            ['Drone', 'Memory_Card'],
            ['Controller', 'Gaming_Console'],
            ['Smart_Watch', 'Earbuds'],
        ],
        'Walmart': [
            ['Milk', 'Bread', 'Eggs'],
            ['Butter', 'Cheese', 'Milk'],
            ['Cereal', 'Milk'],
            ['Coffee', 'Sugar'],
            ['Tea', 'Sugar'],
            ['Flour', 'Sugar', 'Eggs'],
            ['Rice', 'Chicken'],
            ['Pasta', 'Tomato_Sauce', 'Olive_Oil'],
            ['Bread', 'Butter', 'Eggs'],
            ['Chicken', 'Beef', 'Salt', 'Pepper'],
        ],
        'Target': [
            ['T_Shirt', 'Jeans'],
            ['Sneakers', 'Socks'],
            ['Jacket', 'Hat', 'Scarf'],
            ['Backpack', 'Sunglasses'],
            ['Watch', 'Belt', 'Wallet'],
            ['T_Shirt', 'Jeans', 'Sneakers'],
            ['Gloves', 'Scarf', 'Hat'],
            ['Sweater', 'Jeans'],
            ['Dress', 'Sunglasses'],
            ['Belt', 'Wallet'],
        ],
        'Costco': [
            ['Paper_Towels', 'Toilet_Paper'],
            ['Detergent', 'Dish_Soap'],
            ['Shampoo', 'Toothpaste'],
            ['Trash_Bags', 'Batteries'],
            ['Light_Bulbs', 'Batteries'],
            ['Water_Bottles', 'Snacks_Box'],
            ['Frozen_Pizza', 'Snacks_Box'],
            ['Rotisserie_Chicken', 'Muffins'],
            ['Nuts_Pack', 'Water_Bottles'],
            ['Paper_Towels', 'Toilet_Paper', 'Detergent'],
        ],
    }
    
    store_patterns = patterns.get(store_name, [])
    
    # Generate transactions based on patterns and deterministic expansion
    for i in range(num_transactions):
        # Use deterministic selection
        pattern_idx = i % len(store_patterns)
        base_items = store_patterns[pattern_idx].copy()
        
        # Deterministically add more items based on transaction number
        seed = f"{store_name}_{i}"
        hash_val = int(hashlib.md5(seed.encode()).hexdigest(), 16)
        
        # Add 0-3 additional items deterministically
        extra_items_count = (hash_val % 4)
        for j in range(extra_items_count):
            item_idx = (hash_val + j) % len(items)
            extra_item = items[item_idx]
            if extra_item not in base_items:
                base_items.append(extra_item)
        
        transactions.append(base_items)
    
    return transactions

def save_to_csv(store_name, transactions, filename):
    """Save transactions to CSV file"""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['TransactionID', 'Items'])
        
        # Write transactions
        for i, transaction in enumerate(transactions, 1):
            items_str = ','.join(transaction)
            writer.writerow([f'T{i:03d}', items_str])
    
    print(f"✓ Created {filename} with {len(transactions)} transactions")

def main():
    """Generate all databases"""
    print("Generating Transactional Databases...")
    print("=" * 60)
    
    for store_name, items in STORE_ITEMS.items():
        print(f"\n{store_name}:")
        print(f"  Items: {len(items)}")
        
        # Generate transactions
        transactions = generate_deterministic_transactions(store_name, items)
        
        print(f"  Transactions: {len(transactions)}")
        
        # Save to CSV
        filename = f"{store_name}_transactions.csv"
        save_to_csv(store_name, transactions, filename)
        
        # Display sample transactions
        print(f"  Sample transactions:")
        for i in range(min(3, len(transactions))):
            print(f"    T{i+1:03d}: {', '.join(transactions[i])}")
    
    print("\n" + "=" * 60)
    print("All databases generated successfully!")
    print("\nFiles created:")
    for store_name in STORE_ITEMS.keys():
        print(f"  - {store_name}_transactions.csv")

if __name__ == "__main__":
    main()

"""
Automated Brute Force Mining - Runs with default parameters
"""

from brute_force_mining import BruteForceMiner, run_mining_on_database
import time


def main():
    """Run mining on all 5 databases with default parameters"""
    print("="*80)
    print("BRUTE FORCE FREQUENT ITEMSET MINING - ALL DATABASES")
    print("="*80)
    
    # Default parameters
    min_support = 0.2  # 20% support
    min_confidence = 0.6  # 60% confidence
    
    print("\n" + "="*80)
    print("CONFIGURATION")
    print("="*80)
    print(f"  Minimum Support: {min_support} (20%)")
    print(f"  Minimum Confidence: {min_confidence} (60%)")
    print("\nNote: You can modify these in the script or use brute_force_mining.py for interactive input")
    
    # Database configurations
    databases = [
        ('Amazon', 'Amazon_transactions.csv'),
        ('BestBuy', 'BestBuy_transactions.csv'),
        ('Walmart', 'Walmart_transactions.csv'),
        ('Target', 'Target_transactions.csv'),
        ('Costco', 'Costco_transactions.csv')
    ]
    
    # Run mining on each database
    results = {}
    total_start_time = time.time()
    
    for db_name, csv_file in databases:
        miner = run_mining_on_database(db_name, csv_file, min_support, min_confidence)
        results[db_name] = miner
    
    # Summary
    total_elapsed = time.time() - total_start_time
    
    print("\n\n")
    print("="*80)
    print("SUMMARY - ALL DATABASES")
    print("="*80)
    
    print(f"\n{'Database':<15} {'Transactions':<15} {'Items':<10} {'Freq Sets':<12} {'Rules':<10}")
    print("-"*80)
    
    for db_name, miner in results.items():
        num_itemsets = sum(len(v) for v in miner.frequent_itemsets.values())
        num_rules = len(miner.association_rules)
        print(f"{db_name:<15} {miner.num_transactions:<15} {len(miner.all_items):<10} {num_itemsets:<12} {num_rules:<10}")
    
    print("\n" + "="*80)
    print(f"Total execution time: {total_elapsed:.2f} seconds")
    print("="*80)
    
    print("\n✓ All databases processed successfully!")
    print("\nOutput files generated for each database:")
    print("  - {database}_results_frequent_itemsets.txt")
    print("  - {database}_results_association_rules.txt")
    print("  - {database}_results_association_rules.csv")


if __name__ == "__main__":
    main()

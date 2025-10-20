"""
Library-Based Frequent Itemset Mining using Apriori and FP-Growth

This implementation uses Python libraries (mlxtend) to run:
- Apriori algorithm
- FP-Growth algorithm

No custom implementation - uses existing library functions.
"""

import csv
import pandas as pd
import time
from typing import List, Dict


def load_transactions_as_dataframe(csv_file: str):
    """Load transactions and convert to one-hot encoded DataFrame"""
    transactions = []
    
    # Read CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            items = [item.strip() for item in row['Items'].split(',')]
            transactions.append(items)
    
    # Get all unique items
    all_items = set()
    for transaction in transactions:
        all_items.update(transaction)
    
    all_items = sorted(list(all_items))
    
    # Create one-hot encoded DataFrame
    data = []
    for transaction in transactions:
        row = {item: (item in transaction) for item in all_items}
        data.append(row)
    
    df = pd.DataFrame(data)
    
    return df, len(transactions), len(all_items)


def format_itemset(itemset):
    """Format itemset as comma-separated string"""
    if isinstance(itemset, frozenset):
        return ', '.join(sorted(list(itemset)))
    return str(itemset)


def generate_rules_from_library(frequent_itemsets_df, min_confidence, num_transactions):
    """Generate association rules from frequent itemsets"""
    from mlxtend.frequent_patterns import association_rules
    
    if len(frequent_itemsets_df) == 0:
        return pd.DataFrame()
    
    # Generate rules
    try:
        rules = association_rules(frequent_itemsets_df, 
                                  metric="confidence", 
                                  min_threshold=min_confidence)
        return rules
    except ValueError as e:
        # No rules could be generated
        return pd.DataFrame()


def run_apriori(db_name: str, csv_file: str, min_support: float, min_confidence: float):
    """Run Apriori algorithm using mlxtend library"""
    print("\n" + "="*70)
    print(f"APRIORI ALGORITHM - {db_name}")
    print("="*70)
    
    from mlxtend.frequent_patterns import apriori
    
    # Load data
    print(f"\nLoading transactions from: {csv_file}")
    df, num_transactions, num_items = load_transactions_as_dataframe(csv_file)
    print(f"Loaded {num_transactions} transactions")
    print(f"Total unique items: {num_items}")
    
    # Run Apriori
    print(f"\nRunning Apriori with min_support={min_support}...")
    start_time = time.time()
    
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    
    elapsed = time.time() - start_time
    print(f"✓ Apriori completed in {elapsed:.4f} seconds")
    print(f"✓ Found {len(frequent_itemsets)} frequent itemsets")
    
    # Group by size
    if len(frequent_itemsets) > 0:
        frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
        
        print("\nFrequent itemsets by size:")
        for k in sorted(frequent_itemsets['length'].unique()):
            count = len(frequent_itemsets[frequent_itemsets['length'] == k])
            print(f"  {k}-itemsets: {count}")
        
        # Show top 10
        print(f"\nTop 10 frequent itemsets (by support):")
        top_itemsets = frequent_itemsets.nlargest(10, 'support')
        for idx, row in top_itemsets.iterrows():
            items_str = format_itemset(row['itemsets'])
            support = row['support']
            count = int(support * num_transactions)
            print(f"  {{{items_str}}} - Support: {support:.4f}, Count: {count}")
    
    # Generate association rules
    print(f"\nGenerating association rules with min_confidence={min_confidence}...")
    rules = generate_rules_from_library(frequent_itemsets, min_confidence, num_transactions)
    
    if len(rules) > 0:
        print(f"✓ Generated {len(rules)} association rules")
        
        # Show top 10 rules
        print(f"\nTop 10 association rules (by confidence):")
        print("-" * 80)
        print(f"{'Rule':<50} {'Supp':>8} {'Conf':>8} {'Lift':>8}")
        print("-" * 80)
        
        top_rules = rules.nlargest(10, 'confidence')
        for idx, rule in top_rules.iterrows():
            ant_str = format_itemset(rule['antecedents'])
            cons_str = format_itemset(rule['consequents'])
            rule_str = f"{{{ant_str}}} -> {{{cons_str}}}"
            print(f"{rule_str:<50} {rule['support']:>8.4f} {rule['confidence']:>8.4f} {rule['lift']:>8.4f}")
    else:
        print("✓ No association rules generated (no itemsets with 2+ items)")
    
    return frequent_itemsets, rules, elapsed


def run_fpgrowth(db_name: str, csv_file: str, min_support: float, min_confidence: float):
    """Run FP-Growth algorithm using mlxtend library"""
    print("\n" + "="*70)
    print(f"FP-GROWTH ALGORITHM - {db_name}")
    print("="*70)
    
    from mlxtend.frequent_patterns import fpgrowth
    
    # Load data
    print(f"\nLoading transactions from: {csv_file}")
    df, num_transactions, num_items = load_transactions_as_dataframe(csv_file)
    print(f"Loaded {num_transactions} transactions")
    print(f"Total unique items: {num_items}")
    
    # Run FP-Growth
    print(f"\nRunning FP-Growth with min_support={min_support}...")
    start_time = time.time()
    
    frequent_itemsets = fpgrowth(df, min_support=min_support, use_colnames=True)
    
    elapsed = time.time() - start_time
    print(f"✓ FP-Growth completed in {elapsed:.4f} seconds")
    print(f"✓ Found {len(frequent_itemsets)} frequent itemsets")
    
    # Group by size
    if len(frequent_itemsets) > 0:
        frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
        
        print("\nFrequent itemsets by size:")
        for k in sorted(frequent_itemsets['length'].unique()):
            count = len(frequent_itemsets[frequent_itemsets['length'] == k])
            print(f"  {k}-itemsets: {count}")
        
        # Show top 10
        print(f"\nTop 10 frequent itemsets (by support):")
        top_itemsets = frequent_itemsets.nlargest(10, 'support')
        for idx, row in top_itemsets.iterrows():
            items_str = format_itemset(row['itemsets'])
            support = row['support']
            count = int(support * num_transactions)
            print(f"  {{{items_str}}} - Support: {support:.4f}, Count: {count}")
    
    # Generate association rules
    print(f"\nGenerating association rules with min_confidence={min_confidence}...")
    rules = generate_rules_from_library(frequent_itemsets, min_confidence, num_transactions)
    
    if len(rules) > 0:
        print(f"✓ Generated {len(rules)} association rules")
        
        # Show top 10 rules
        print(f"\nTop 10 association rules (by confidence):")
        print("-" * 80)
        print(f"{'Rule':<50} {'Supp':>8} {'Conf':>8} {'Lift':>8}")
        print("-" * 80)
        
        top_rules = rules.nlargest(10, 'confidence')
        for idx, rule in top_rules.iterrows():
            ant_str = format_itemset(rule['antecedents'])
            cons_str = format_itemset(rule['consequents'])
            rule_str = f"{{{ant_str}}} -> {{{cons_str}}}"
            print(f"{rule_str:<50} {rule['support']:>8.4f} {rule['confidence']:>8.4f} {rule['lift']:>8.4f}")
    else:
        print("✓ No association rules generated (no itemsets with 2+ items)")
    
    return frequent_itemsets, rules, elapsed


def save_results(db_name: str, algorithm: str, frequent_itemsets, rules, num_transactions):
    """Save results to files"""
    prefix = f"{db_name}_{algorithm.lower()}_results"
    
    # Save frequent itemsets
    itemsets_file = f"{prefix}_frequent_itemsets.txt"
    with open(itemsets_file, 'w', encoding='utf-8') as f:
        f.write(f"FREQUENT ITEMSETS - {algorithm.upper()}\n")
        f.write("="*70 + "\n\n")
        f.write(f"Algorithm: {algorithm}\n")
        f.write(f"Total Itemsets: {len(frequent_itemsets)}\n\n")
        
        if len(frequent_itemsets) > 0:
            # Group by length
            for k in sorted(frequent_itemsets['length'].unique()):
                k_itemsets = frequent_itemsets[frequent_itemsets['length'] == k]
                k_itemsets = k_itemsets.sort_values('support', ascending=False)
                
                f.write(f"\n{k}-Itemsets ({len(k_itemsets)} frequent):\n")
                f.write("-"*70 + "\n")
                
                for idx, row in k_itemsets.iterrows():
                    items_str = format_itemset(row['itemsets'])
                    support = row['support']
                    count = int(support * num_transactions)
                    f.write(f"{{{items_str}}} - Support: {support:.4f}, Count: {count}\n")
    
    print(f"  ✓ Saved itemsets to: {itemsets_file}")
    
    # Save association rules
    if len(rules) > 0:
        rules_file = f"{prefix}_association_rules.txt"
        with open(rules_file, 'w', encoding='utf-8') as f:
            f.write(f"ASSOCIATION RULES - {algorithm.upper()}\n")
            f.write("="*70 + "\n\n")
            f.write(f"Algorithm: {algorithm}\n")
            f.write(f"Total Rules: {len(rules)}\n\n")
            
            f.write(f"{'Rule':<50} {'Supp':>8} {'Conf':>8} {'Lift':>8}\n")
            f.write("-"*80 + "\n")
            
            rules_sorted = rules.sort_values('confidence', ascending=False)
            for idx, rule in rules_sorted.iterrows():
                ant_str = format_itemset(rule['antecedents'])
                cons_str = format_itemset(rule['consequents'])
                rule_str = f"{{{ant_str}}} -> {{{cons_str}}}"
                f.write(f"{rule_str:<50} {rule['support']:>8.4f} {rule['confidence']:>8.4f} {rule['lift']:>8.4f}\n")
        
        print(f"  ✓ Saved rules to: {rules_file}")
        
        # Save CSV
        rules_csv = f"{prefix}_association_rules.csv"
        rules_export = rules.copy()
        rules_export['antecedents'] = rules_export['antecedents'].apply(format_itemset)
        rules_export['consequents'] = rules_export['consequents'].apply(format_itemset)
        rules_export[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_csv(
            rules_csv, index=False
        )
        print(f"  ✓ Saved rules CSV to: {rules_csv}")
    else:
        print(f"  (No rules to save)")


def run_all_databases(min_support: float = 0.2, min_confidence: float = 0.6):
    """Run both algorithms on all databases"""
    
    print("="*80)
    print("LIBRARY-BASED MINING: APRIORI AND FP-GROWTH")
    print("="*80)
    print(f"\nConfiguration:")
    print(f"  Minimum Support: {min_support}")
    print(f"  Minimum Confidence: {min_confidence}")
    print(f"  Libraries: mlxtend (scikit-learn ecosystem)")
    
    databases = [
        ('Amazon', 'Amazon_transactions.csv'),
        ('BestBuy', 'BestBuy_transactions.csv'),
        ('Walmart', 'Walmart_transactions.csv'),
        ('Target', 'Target_transactions.csv'),
        ('Costco', 'Costco_transactions.csv')
    ]
    
    results = {
        'apriori': {},
        'fpgrowth': {}
    }
    
    total_start = time.time()
    
    # Run both algorithms on each database
    for db_name, csv_file in databases:
        print("\n\n" + "#"*80)
        print(f"# DATABASE: {db_name}")
        print("#"*80)
        
        # Load transaction count for reporting
        df, num_trans, num_items = load_transactions_as_dataframe(csv_file)
        
        # Run Apriori
        apriori_itemsets, apriori_rules, apriori_time = run_apriori(
            db_name, csv_file, min_support, min_confidence
        )
        
        # Save Apriori results
        print("\nSaving Apriori results...")
        save_results(db_name, 'Apriori', apriori_itemsets, apriori_rules, num_trans)
        
        # Run FP-Growth
        fpgrowth_itemsets, fpgrowth_rules, fpgrowth_time = run_fpgrowth(
            db_name, csv_file, min_support, min_confidence
        )
        
        # Save FP-Growth results
        print("\nSaving FP-Growth results...")
        save_results(db_name, 'FPGrowth', fpgrowth_itemsets, fpgrowth_rules, num_trans)
        
        # Store results
        results['apriori'][db_name] = {
            'itemsets': len(apriori_itemsets),
            'rules': len(apriori_rules),
            'time': apriori_time,
            'transactions': num_trans,
            'items': num_items
        }
        results['fpgrowth'][db_name] = {
            'itemsets': len(fpgrowth_itemsets),
            'rules': len(fpgrowth_rules),
            'time': fpgrowth_time,
            'transactions': num_trans,
            'items': num_items
        }
    
    total_time = time.time() - total_start
    
    # Summary
    print("\n\n" + "="*80)
    print("SUMMARY - COMPARISON OF ALGORITHMS")
    print("="*80)
    
    print("\n--- APRIORI RESULTS ---")
    print(f"{'Database':<15} {'Trans':<8} {'Items':<8} {'Itemsets':<10} {'Rules':<8} {'Time(s)':<10}")
    print("-"*80)
    for db_name in results['apriori'].keys():
        r = results['apriori'][db_name]
        print(f"{db_name:<15} {r['transactions']:<8} {r['items']:<8} {r['itemsets']:<10} {r['rules']:<8} {r['time']:<10.4f}")
    
    apriori_total_itemsets = sum(r['itemsets'] for r in results['apriori'].values())
    apriori_total_rules = sum(r['rules'] for r in results['apriori'].values())
    apriori_total_time = sum(r['time'] for r in results['apriori'].values())
    print("-"*80)
    print(f"{'TOTAL':<15} {'':<8} {'':<8} {apriori_total_itemsets:<10} {apriori_total_rules:<8} {apriori_total_time:<10.4f}")
    
    print("\n--- FP-GROWTH RESULTS ---")
    print(f"{'Database':<15} {'Trans':<8} {'Items':<8} {'Itemsets':<10} {'Rules':<8} {'Time(s)':<10}")
    print("-"*80)
    for db_name in results['fpgrowth'].keys():
        r = results['fpgrowth'][db_name]
        print(f"{db_name:<15} {r['transactions']:<8} {r['items']:<8} {r['itemsets']:<10} {r['rules']:<8} {r['time']:<10.4f}")
    
    fpgrowth_total_itemsets = sum(r['itemsets'] for r in results['fpgrowth'].values())
    fpgrowth_total_rules = sum(r['rules'] for r in results['fpgrowth'].values())
    fpgrowth_total_time = sum(r['time'] for r in results['fpgrowth'].values())
    print("-"*80)
    print(f"{'TOTAL':<15} {'':<8} {'':<8} {fpgrowth_total_itemsets:<10} {fpgrowth_total_rules:<8} {fpgrowth_total_time:<10.4f}")
    
    print("\n--- PERFORMANCE COMPARISON ---")
    print(f"Apriori total time:    {apriori_total_time:.4f} seconds")
    print(f"FP-Growth total time:  {fpgrowth_total_time:.4f} seconds")
    if fpgrowth_total_time > 0:
        speedup = apriori_total_time / fpgrowth_total_time
        print(f"Speedup (Apriori/FPGrowth): {speedup:.2f}x")
    
    print("\n" + "="*80)
    print(f"Total execution time: {total_time:.2f} seconds")
    print("="*80)
    
    print("\n✓ All databases processed with both algorithms!")
    print("\nOutput files generated for each database:")
    print("  Apriori:")
    print("    - {database}_apriori_results_frequent_itemsets.txt")
    print("    - {database}_apriori_results_association_rules.txt")
    print("    - {database}_apriori_results_association_rules.csv")
    print("  FP-Growth:")
    print("    - {database}_fpgrowth_results_frequent_itemsets.txt")
    print("    - {database}_fpgrowth_results_association_rules.txt")
    print("    - {database}_fpgrowth_results_association_rules.csv")


def check_dependencies():
    """Check if required libraries are installed"""
    try:
        import mlxtend
        print(f"✓ mlxtend version: {mlxtend.__version__}")
        return True
    except ImportError:
        print("ERROR: mlxtend library not found!")
        print("\nPlease install it using:")
        print("  pip install mlxtend")
        return False


def main():
    """Main function"""
    print("Checking dependencies...")
    if not check_dependencies():
        return
    
    print("✓ All dependencies found\n")
    
    # Run with default parameters
    min_support = 0.2
    min_confidence = 0.6
    
    run_all_databases(min_support, min_confidence)


if __name__ == "__main__":
    main()

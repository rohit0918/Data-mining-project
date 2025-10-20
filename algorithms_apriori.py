"""
Apriori Algorithm for Frequent Itemset Mining
This module can be executed standalone or imported
"""

import csv
import time
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


def load_transactions(csv_file):
    """Load transactions from CSV file"""
    transactions = []
    all_items = set()
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            items = [item.strip() for item in row['Items'].split(',')]
            transactions.append(frozenset(items))
            all_items.update(items)
    
    return transactions, all_items


def run_apriori(transactions, all_items, min_support, min_confidence):
    """
    Run Apriori algorithm using mlxtend library
    
    Parameters:
    -----------
    transactions : list
        Transaction database
    all_items : set
        Set of all unique items
    min_support : float
        Minimum support threshold
    min_confidence : float
        Minimum confidence threshold
    
    Returns:
    --------
    frequent_itemsets_df : DataFrame
        DataFrame of frequent itemsets
    rules_df : DataFrame
        DataFrame of association rules
    elapsed_time : float
        Execution time in seconds
    """
    print("🔍 Running Apriori Algorithm...\n")
    
    start_time = time.time()
    
    # Convert transactions to DataFrame format (one-hot encoding)
    all_items_sorted = sorted(list(all_items))
    data = []
    for transaction in transactions:
        row = {item: (item in transaction) for item in all_items_sorted}
        data.append(row)
    df = pd.DataFrame(data)
    
    # Run Apriori
    frequent_itemsets_df = apriori(df, min_support=min_support, use_colnames=True)
    
    if len(frequent_itemsets_df) > 0:
        frequent_itemsets_df['length'] = frequent_itemsets_df['itemsets'].apply(lambda x: len(x))
    
    elapsed_time = time.time() - start_time
    
    print(f"⏱️  Execution Time: {elapsed_time:.4f} seconds")
    print(f"📊 Total Frequent Itemsets: {len(frequent_itemsets_df)}")
    
    # Generate association rules
    rules_df = None
    if len(frequent_itemsets_df) > 0:
        try:
            rules_df = association_rules(
                frequent_itemsets_df, 
                metric="confidence", 
                min_threshold=min_confidence
            )
        except:
            print("⚠️  No association rules generated (need itemsets with 2+ items)")
    
    return frequent_itemsets_df, rules_df, elapsed_time


def display_results(frequent_itemsets_df, rules_df, num_transactions):
    """Display mining results"""
    print("\n" + "="*80)
    print("FREQUENT ITEMSETS")
    print("="*80)
    
    if len(frequent_itemsets_df) > 0:
        for k in sorted(frequent_itemsets_df['length'].unique()):
            k_itemsets = frequent_itemsets_df[frequent_itemsets_df['length'] == k].sort_values('support', ascending=False)
            print(f"\n📦 {k}-Itemsets ({len(k_itemsets)} found):")
            for idx, row in k_itemsets.head(10).iterrows():
                items_str = ', '.join(sorted(list(row['itemsets'])))
                support = row['support']
                count = int(support * num_transactions)
                print(f"   {{{items_str}}} - Count: {count}, Support: {support:.4f}")
            if len(k_itemsets) > 10:
                print(f"   ... and {len(k_itemsets) - 10} more")
    
    print("\n" + "="*80)
    print("ASSOCIATION RULES")
    print("="*80)
    
    if rules_df is not None and len(rules_df) > 0:
        print(f"\nTotal Rules Generated: {len(rules_df)}")
        print(f"\nTop 15 Rules:")
        print(f"\n{'Rule':<60} {'Supp':>8} {'Conf':>8} {'Lift':>8}")
        print("-"*90)
        sorted_rules = rules_df.sort_values('confidence', ascending=False).head(15)
        for idx, rule in sorted_rules.iterrows():
            ant_str = ', '.join(sorted(list(rule['antecedents'])))
            cons_str = ', '.join(sorted(list(rule['consequents'])))
            rule_str = f"{{{ant_str}}} → {{{cons_str}}}"
            print(f"{rule_str:<60} {rule['support']:>8.4f} {rule['confidence']:>8.4f} {rule['lift']:>8.4f}")
        if len(rules_df) > 15:
            print(f"\n... and {len(rules_df) - 15} more rules")
    else:
        print("\nNo association rules generated.")


if __name__ == "__main__":
    # Example usage
    print("\n" + "="*80)
    print("APRIORI ALGORITHM - STANDALONE EXECUTION")
    print("="*80)
    
    # Configuration
    database_file = "data/Amazon_transactions.csv"
    min_support = 0.2
    min_confidence = 0.6
    
    # Load data
    print(f"\n📂 Loading database: {database_file}")
    transactions, all_items = load_transactions(database_file)
    print(f"✅ Loaded {len(transactions)} transactions with {len(all_items)} unique items")
    
    # Run algorithm
    frequent_itemsets_df, rules_df, exec_time = run_apriori(
        transactions, all_items, min_support, min_confidence
    )
    
    # Display results
    display_results(frequent_itemsets_df, rules_df, len(transactions))
    
    print("\n" + "="*80)
    print("✅ APRIORI ANALYSIS COMPLETE!")
    print("="*80)

"""
Brute Force Algorithm for Frequent Itemset Mining
This module can be executed standalone or imported
"""

import csv
import time
from itertools import combinations


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


def get_support_count(itemset, transactions):
    """Count how many transactions contain the itemset"""
    count = 0
    for transaction in transactions:
        if itemset.issubset(transaction):
            count += 1
    return count


def is_frequent(itemset, transactions, min_support):
    """Check if itemset meets minimum support threshold"""
    support_count = get_support_count(itemset, transactions)
    if min_support < 1:
        return support_count >= (min_support * len(transactions))
    else:
        return support_count >= min_support


def brute_force_mining(transactions, all_items, min_support):
    """
    Brute Force algorithm for frequent itemset mining
    
    Parameters:
    -----------
    transactions : list of frozenset
        Transaction database
    all_items : set
        Set of all unique items
    min_support : float
        Minimum support threshold
    
    Returns:
    --------
    frequent_itemsets : dict
        Dictionary mapping k to list of (itemset, count) tuples
    elapsed_time : float
        Execution time in seconds
    """
    print("🔍 Running Brute Force Algorithm...\n")
    
    start_time = time.time()
    items_list = sorted(list(all_items))
    frequent_itemsets = {}
    k = 1
    
    while True:
        print(f"Checking {k}-itemsets...", end=' ')
        
        # Generate all k-itemsets
        all_k_itemsets = [frozenset(comb) for comb in combinations(items_list, k)]
        
        # Check frequency
        frequent_k = []
        for itemset in all_k_itemsets:
            if is_frequent(itemset, transactions, min_support):
                support_count = get_support_count(itemset, transactions)
                frequent_k.append((itemset, support_count))
        
        if not frequent_k:
            print(f"Found 0 frequent {k}-itemsets. Stopping.")
            break
        
        print(f"Found {len(frequent_k)} frequent {k}-itemsets ✓")
        frequent_itemsets[k] = frequent_k
        k += 1
    
    elapsed_time = time.time() - start_time
    
    print(f"\n⏱️  Execution Time: {elapsed_time:.4f} seconds")
    print(f"📊 Total Frequent Itemsets: {sum(len(v) for v in frequent_itemsets.values())}")
    
    return frequent_itemsets, elapsed_time


def generate_association_rules(frequent_itemsets, transactions, min_confidence):
    """
    Generate association rules from frequent itemsets
    
    Parameters:
    -----------
    frequent_itemsets : dict
        Dictionary of frequent itemsets
    transactions : list
        Transaction database
    min_confidence : float
        Minimum confidence threshold
    
    Returns:
    --------
    rules : list of dict
        List of association rules with metrics
    """
    rules = []
    num_transactions = len(transactions)
    
    for k in range(2, max(frequent_itemsets.keys()) + 1):
        if k not in frequent_itemsets:
            continue
        
        for itemset, support_count in frequent_itemsets[k]:
            items = list(itemset)
            
            for i in range(1, len(items)):
                for antecedent_items in combinations(items, i):
                    antecedent = frozenset(antecedent_items)
                    consequent = itemset - antecedent
                    
                    antecedent_support_count = get_support_count(antecedent, transactions)
                    
                    if antecedent_support_count == 0:
                        continue
                    
                    confidence = support_count / antecedent_support_count
                    
                    if confidence >= min_confidence:
                        support = support_count / num_transactions
                        consequent_support = get_support_count(consequent, transactions) / num_transactions
                        lift = confidence / consequent_support if consequent_support > 0 else 0
                        
                        rules.append({
                            'antecedent': antecedent,
                            'consequent': consequent,
                            'support': support,
                            'confidence': confidence,
                            'lift': lift
                        })
    
    return sorted(rules, key=lambda x: (x['confidence'], x['support']), reverse=True)


def display_results(frequent_itemsets, rules, num_transactions):
    """Display mining results"""
    print("\n" + "="*80)
    print("FREQUENT ITEMSETS")
    print("="*80)
    
    for k in sorted(frequent_itemsets.keys()):
        itemsets = frequent_itemsets[k]
        print(f"\n📦 {k}-Itemsets ({len(itemsets)} found):")
        sorted_itemsets = sorted(itemsets, key=lambda x: x[1], reverse=True)
        for itemset, count in sorted_itemsets[:10]:
            support = count / num_transactions
            items_str = ', '.join(sorted(list(itemset)))
            print(f"   {{{items_str}}} - Count: {count}, Support: {support:.4f}")
        if len(sorted_itemsets) > 10:
            print(f"   ... and {len(sorted_itemsets) - 10} more")
    
    print("\n" + "="*80)
    print("ASSOCIATION RULES")
    print("="*80)
    print(f"\nTotal Rules Generated: {len(rules)}")
    
    if rules:
        print(f"\nTop 15 Rules:")
        print(f"\n{'Rule':<60} {'Supp':>8} {'Conf':>8} {'Lift':>8}")
        print("-"*90)
        for rule in rules[:15]:
            ant_str = ', '.join(sorted(list(rule['antecedent'])))
            cons_str = ', '.join(sorted(list(rule['consequent'])))
            rule_str = f"{{{ant_str}}} → {{{cons_str}}}"
            print(f"{rule_str:<60} {rule['support']:>8.4f} {rule['confidence']:>8.4f} {rule['lift']:>8.4f}")
        if len(rules) > 15:
            print(f"\n... and {len(rules) - 15} more rules")


if __name__ == "__main__":
    # Example usage
    print("\n" + "="*80)
    print("BRUTE FORCE ALGORITHM - STANDALONE EXECUTION")
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
    frequent_itemsets, exec_time = brute_force_mining(transactions, all_items, min_support)
    
    # Generate rules
    rules = generate_association_rules(frequent_itemsets, transactions, min_confidence)
    
    # Display results
    display_results(frequent_itemsets, rules, len(transactions))
    
    print("\n" + "="*80)
    print("✅ BRUTE FORCE ANALYSIS COMPLETE!")
    print("="*80)

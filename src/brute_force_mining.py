"""
Brute Force Frequent Itemset Mining and Association Rule Generation

This implementation uses a brute force approach:
- Enumerates ALL possible k-itemsets for k=1,2,3,...
- Checks each against minimum support threshold
- Stops when no frequent k-itemsets are found
- Generates association rules from frequent itemsets
"""

import csv
from itertools import combinations
from typing import List, Set, Tuple, Dict
import time


class BruteForceMiner:
    """Brute force frequent itemset mining"""
    
    def __init__(self, min_support: float, min_confidence: float):
        """
        Initialize miner with minimum support and confidence thresholds
        
        Args:
            min_support: Minimum support threshold (0-1 or absolute count)
            min_confidence: Minimum confidence threshold (0-1)
        """
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.transactions = []
        self.num_transactions = 0
        self.all_items = set()
        self.frequent_itemsets = {}  # {k: [(itemset, support_count)]}
        self.association_rules = []
        
    def load_transactions(self, csv_file: str):
        """Load transactions from CSV file"""
        self.transactions = []
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse items from the Items column
                items = [item.strip() for item in row['Items'].split(',')]
                self.transactions.append(frozenset(items))
                self.all_items.update(items)
        
        self.num_transactions = len(self.transactions)
        print(f"Loaded {self.num_transactions} transactions")
        print(f"Total unique items: {len(self.all_items)}")
        
    def get_support_count(self, itemset: frozenset) -> int:
        """Count how many transactions contain the itemset"""
        count = 0
        for transaction in self.transactions:
            if itemset.issubset(transaction):
                count += 1
        return count
    
    def get_support(self, itemset: frozenset) -> float:
        """Calculate support (fraction of transactions containing itemset)"""
        return self.get_support_count(itemset) / self.num_transactions
    
    def is_frequent(self, itemset: frozenset) -> bool:
        """Check if itemset meets minimum support threshold"""
        support_count = self.get_support_count(itemset)
        
        # Handle both absolute and relative support
        if self.min_support < 1:
            # Relative support (fraction)
            return support_count >= (self.min_support * self.num_transactions)
        else:
            # Absolute support (count)
            return support_count >= self.min_support
    
    def find_frequent_itemsets(self):
        """
        Brute force algorithm to find all frequent itemsets
        
        Process:
        1. Generate all possible k-itemsets for k=1,2,3,...
        2. Check each against minimum support
        3. Stop when no frequent k-itemsets found
        """
        print("\n" + "="*70)
        print("BRUTE FORCE FREQUENT ITEMSET MINING")
        print("="*70)
        
        items_list = sorted(list(self.all_items))
        k = 1
        
        while True:
            print(f"\n--- Finding {k}-itemsets ---")
            
            # Generate ALL possible k-itemsets (brute force - no pruning)
            all_k_itemsets = [frozenset(comb) for comb in combinations(items_list, k)]
            total_possible = len(all_k_itemsets)
            
            print(f"Total possible {k}-itemsets: {total_possible}")
            
            # Check each k-itemset for frequency
            frequent_k_itemsets = []
            checked_count = 0
            
            for itemset in all_k_itemsets:
                checked_count += 1
                if checked_count % 1000 == 0:
                    print(f"  Checked {checked_count}/{total_possible}...", end='\r')
                
                if self.is_frequent(itemset):
                    support_count = self.get_support_count(itemset)
                    frequent_k_itemsets.append((itemset, support_count))
            
            # Clear progress line
            if total_possible >= 1000:
                print(" " * 60, end='\r')
            
            num_frequent = len(frequent_k_itemsets)
            print(f"Found {num_frequent} frequent {k}-itemsets")
            
            # If no frequent k-itemsets found, stop
            if num_frequent == 0:
                print(f"\nNo frequent {k}-itemsets found. Terminating.")
                break
            
            # Store frequent k-itemsets
            self.frequent_itemsets[k] = frequent_k_itemsets
            
            # Display top 10 frequent k-itemsets
            if num_frequent > 0:
                print(f"\nTop frequent {k}-itemsets:")
                # Sort by support count descending
                sorted_itemsets = sorted(frequent_k_itemsets, 
                                        key=lambda x: x[1], 
                                        reverse=True)
                for itemset, count in sorted_itemsets[:10]:
                    support = count / self.num_transactions
                    items_str = ', '.join(sorted(list(itemset)))
                    print(f"  {{{items_str}}} - Count: {count}, Support: {support:.3f}")
            
            k += 1
        
        print("\n" + "="*70)
        print(f"Total frequent itemsets found: {sum(len(v) for v in self.frequent_itemsets.values())}")
        print("="*70)
    
    def generate_association_rules(self):
        """
        Generate association rules from frequent itemsets
        
        For each frequent itemset with |itemset| >= 2:
        - Generate all possible rules A -> B where A ∪ B = itemset
        - Calculate confidence and check against threshold
        """
        print("\n" + "="*70)
        print("GENERATING ASSOCIATION RULES")
        print("="*70)
        
        self.association_rules = []
        
        # Start from 2-itemsets (rules need at least 2 items)
        for k in range(2, max(self.frequent_itemsets.keys()) + 1):
            if k not in self.frequent_itemsets:
                continue
            
            print(f"\n--- Processing {k}-itemsets for rules ---")
            
            for itemset, support_count in self.frequent_itemsets[k]:
                # Generate all possible non-empty proper subsets as antecedents
                items = list(itemset)
                
                # Try all possible splits (1 to k-1 items as antecedent)
                for i in range(1, len(items)):
                    for antecedent_items in combinations(items, i):
                        antecedent = frozenset(antecedent_items)
                        consequent = itemset - antecedent
                        
                        # Calculate confidence: support(A ∪ B) / support(A)
                        antecedent_support_count = self.get_support_count(antecedent)
                        
                        if antecedent_support_count == 0:
                            continue
                        
                        confidence = support_count / antecedent_support_count
                        
                        # Check if rule meets minimum confidence
                        if confidence >= self.min_confidence:
                            support = support_count / self.num_transactions
                            lift = confidence / (self.get_support(consequent))
                            
                            self.association_rules.append({
                                'antecedent': antecedent,
                                'consequent': consequent,
                                'support': support,
                                'confidence': confidence,
                                'lift': lift,
                                'support_count': support_count
                            })
        
        # Sort rules by confidence (descending), then support
        self.association_rules.sort(key=lambda x: (x['confidence'], x['support']), 
                                    reverse=True)
        
        print(f"\nTotal association rules generated: {len(self.association_rules)}")
        
        # Display top rules
        if len(self.association_rules) > 0:
            print(f"\nTop 15 association rules (by confidence):")
            print("-" * 90)
            print(f"{'Rule':<50} {'Supp':>8} {'Conf':>8} {'Lift':>8}")
            print("-" * 90)
            
            for i, rule in enumerate(self.association_rules[:15]):
                ant_str = ', '.join(sorted(list(rule['antecedent'])))
                cons_str = ', '.join(sorted(list(rule['consequent'])))
                rule_str = f"{{{ant_str}}} -> {{{cons_str}}}"
                
                print(f"{rule_str:<50} {rule['support']:>8.3f} {rule['confidence']:>8.3f} {rule['lift']:>8.3f}")
        
        print("="*70)
    
    def save_results(self, output_prefix: str):
        """Save frequent itemsets and rules to files"""
        
        # Save frequent itemsets
        itemsets_file = f"{output_prefix}_frequent_itemsets.txt"
        with open(itemsets_file, 'w', encoding='utf-8') as f:
            f.write("FREQUENT ITEMSETS\n")
            f.write("="*70 + "\n\n")
            f.write(f"Minimum Support: {self.min_support}\n")
            f.write(f"Total Transactions: {self.num_transactions}\n\n")
            
            for k in sorted(self.frequent_itemsets.keys()):
                f.write(f"\n{k}-Itemsets ({len(self.frequent_itemsets[k])} frequent):\n")
                f.write("-"*70 + "\n")
                
                sorted_itemsets = sorted(self.frequent_itemsets[k], 
                                        key=lambda x: x[1], 
                                        reverse=True)
                
                for itemset, count in sorted_itemsets:
                    support = count / self.num_transactions
                    items_str = ', '.join(sorted(list(itemset)))
                    f.write(f"{{{items_str}}} - Count: {count}, Support: {support:.4f}\n")
        
        print(f"\n✓ Saved frequent itemsets to: {itemsets_file}")
        
        # Save association rules
        rules_file = f"{output_prefix}_association_rules.txt"
        with open(rules_file, 'w', encoding='utf-8') as f:
            f.write("ASSOCIATION RULES\n")
            f.write("="*70 + "\n\n")
            f.write(f"Minimum Support: {self.min_support}\n")
            f.write(f"Minimum Confidence: {self.min_confidence}\n")
            f.write(f"Total Rules: {len(self.association_rules)}\n\n")
            
            f.write(f"{'Rule':<50} {'Supp':>8} {'Conf':>8} {'Lift':>8}\n")
            f.write("-"*90 + "\n")
            
            for rule in self.association_rules:
                ant_str = ', '.join(sorted(list(rule['antecedent'])))
                cons_str = ', '.join(sorted(list(rule['consequent'])))
                rule_str = f"{{{ant_str}}} -> {{{cons_str}}}"
                
                f.write(f"{rule_str:<50} {rule['support']:>8.4f} {rule['confidence']:>8.4f} {rule['lift']:>8.4f}\n")
        
        print(f"✓ Saved association rules to: {rules_file}")
        
        # Save CSV for rules (easier to analyze)
        rules_csv = f"{output_prefix}_association_rules.csv"
        with open(rules_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Antecedent', 'Consequent', 'Support', 'Confidence', 'Lift'])
            
            for rule in self.association_rules:
                ant_str = ','.join(sorted(list(rule['antecedent'])))
                cons_str = ','.join(sorted(list(rule['consequent'])))
                writer.writerow([ant_str, cons_str, 
                               f"{rule['support']:.4f}",
                               f"{rule['confidence']:.4f}",
                               f"{rule['lift']:.4f}"])
        
        print(f"✓ Saved association rules CSV to: {rules_csv}")


def run_mining_on_database(db_name: str, csv_file: str, min_support: float, min_confidence: float):
    """Run brute force mining on a single database"""
    print("\n\n")
    print("#"*80)
    print(f"# DATABASE: {db_name}")
    print("#"*80)
    
    start_time = time.time()
    
    # Create miner
    miner = BruteForceMiner(min_support, min_confidence)
    
    # Load data
    print(f"\nLoading transactions from: {csv_file}")
    miner.load_transactions(csv_file)
    
    # Find frequent itemsets
    miner.find_frequent_itemsets()
    
    # Generate association rules
    miner.generate_association_rules()
    
    # Save results
    output_prefix = f"{db_name}_results"
    miner.save_results(output_prefix)
    
    elapsed_time = time.time() - start_time
    print(f"\n✓ Completed {db_name} in {elapsed_time:.2f} seconds")
    
    return miner


def main():
    """Main function to run mining on all 5 databases"""
    print("="*80)
    print("BRUTE FORCE FREQUENT ITEMSET MINING - ALL DATABASES")
    print("="*80)
    
    # User configurable parameters
    print("\n" + "="*80)
    print("CONFIGURATION")
    print("="*80)
    
    # Get user input
    while True:
        try:
            min_support_input = input("\nEnter minimum support (0-1 for percentage, or integer for absolute count) [default: 0.2]: ").strip()
            if min_support_input == "":
                min_support = 0.2
            else:
                min_support = float(min_support_input)
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    while True:
        try:
            min_confidence_input = input("Enter minimum confidence (0-1) [default: 0.6]: ").strip()
            if min_confidence_input == "":
                min_confidence = 0.6
            else:
                min_confidence = float(min_confidence_input)
            
            if 0 <= min_confidence <= 1:
                break
            else:
                print("Confidence must be between 0 and 1.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 1.")
    
    print(f"\nUsing parameters:")
    print(f"  Minimum Support: {min_support}")
    print(f"  Minimum Confidence: {min_confidence}")
    
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

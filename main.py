"""
Interactive Frequent Itemset Mining Tool

Main interactive interface for running mining algorithms on transactional databases.
Results are displayed in the terminal - no files are saved.
"""

import csv
import sys
import os
from itertools import combinations
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


class InteractiveMiner:
    """Interactive mining interface"""
    
    def __init__(self):
        self.databases = {
            '1': ('Amazon', 'data/Amazon_transactions.csv', 'Technology & Electronics'),
            '2': ('BestBuy', 'data/BestBuy_transactions.csv', 'Consumer Electronics'),
            '3': ('Walmart', 'data/Walmart_transactions.csv', 'Groceries'),
            '4': ('Target', 'data/Target_transactions.csv', 'Clothing & Fashion'),
            '5': ('Costco', 'data/Costco_transactions.csv', 'Household Items')
        }
        
        self.algorithms = {
            '1': ('Brute Force', self.run_brute_force),
            '2': ('Apriori', self.run_apriori),
            '3': ('FP-Growth', self.run_fpgrowth)
        }
        
        self.transactions = []
        self.num_transactions = 0
        self.all_items = set()
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "="*80)
        print(f"  {title}")
        print("="*80)
    
    def print_section(self, title):
        """Print a section header"""
        print("\n" + "-"*80)
        print(f"  {title}")
        print("-"*80)
    
    def load_transactions(self, csv_file):
        """Load transactions from CSV"""
        self.transactions = []
        self.all_items = set()
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                items = [item.strip() for item in row['Items'].split(',')]
                self.transactions.append(frozenset(items))
                self.all_items.update(items)
        
        self.num_transactions = len(self.transactions)
    
    def get_support_count(self, itemset):
        """Count support for an itemset"""
        count = 0
        for transaction in self.transactions:
            if itemset.issubset(transaction):
                count += 1
        return count
    
    def is_frequent(self, itemset, min_support):
        """Check if itemset is frequent"""
        support_count = self.get_support_count(itemset)
        if min_support < 1:
            return support_count >= (min_support * self.num_transactions)
        else:
            return support_count >= min_support
    
    def run_brute_force(self, min_support, min_confidence):
        """Run brute force algorithm"""
        print("\n🔍 Running Brute Force Algorithm...")
        start_time = time.time()
        
        items_list = sorted(list(self.all_items))
        frequent_itemsets = {}
        k = 1
        
        while True:
            print(f"\n  Checking {k}-itemsets...", end=' ')
            
            # Generate all k-itemsets
            all_k_itemsets = [frozenset(comb) for comb in combinations(items_list, k)]
            
            # Check frequency
            frequent_k = []
            for itemset in all_k_itemsets:
                if self.is_frequent(itemset, min_support):
                    support_count = self.get_support_count(itemset)
                    frequent_k.append((itemset, support_count))
            
            if not frequent_k:
                print(f"Found 0 frequent {k}-itemsets. Stopping.")
                break
            
            print(f"Found {len(frequent_k)} frequent {k}-itemsets ✓")
            frequent_itemsets[k] = frequent_k
            k += 1
        
        elapsed = time.time() - start_time
        
        # Display results
        self.display_frequent_itemsets(frequent_itemsets)
        rules = self.generate_rules(frequent_itemsets, min_confidence)
        self.display_rules(rules)
        
        print(f"\n⏱️  Execution time: {elapsed:.4f} seconds")
        
        return frequent_itemsets, rules
    
    def run_apriori(self, min_support, min_confidence):
        """Run Apriori using mlxtend"""
        try:
            import pandas as pd
            from mlxtend.frequent_patterns import apriori, association_rules
        except ImportError:
            print("\n❌ Error: mlxtend library not found!")
            print("   Install with: pip install mlxtend")
            return None, None
        
        print("\n🔍 Running Apriori Algorithm...")
        start_time = time.time()
        
        # Convert to DataFrame
        all_items = sorted(list(self.all_items))
        data = []
        for transaction in self.transactions:
            row = {item: (item in transaction) for item in all_items}
            data.append(row)
        df = pd.DataFrame(data)
        
        # Run Apriori
        frequent_itemsets_df = apriori(df, min_support=min_support, use_colnames=True)
        
        if len(frequent_itemsets_df) > 0:
            frequent_itemsets_df['length'] = frequent_itemsets_df['itemsets'].apply(lambda x: len(x))
        
        elapsed = time.time() - start_time
        
        # Display results
        self.display_apriori_results(frequent_itemsets_df)
        
        # Generate rules
        if len(frequent_itemsets_df) > 0:
            try:
                rules_df = association_rules(frequent_itemsets_df, metric="confidence", min_threshold=min_confidence)
                self.display_apriori_rules(rules_df)
            except:
                print("\n  No association rules generated (need itemsets with 2+ items)")
                rules_df = None
        else:
            rules_df = None
        
        print(f"\n⏱️  Execution time: {elapsed:.4f} seconds")
        
        return frequent_itemsets_df, rules_df
    
    def run_fpgrowth(self, min_support, min_confidence):
        """Run FP-Growth using mlxtend"""
        try:
            import pandas as pd
            from mlxtend.frequent_patterns import fpgrowth, association_rules
        except ImportError:
            print("\n❌ Error: mlxtend library not found!")
            print("   Install with: pip install mlxtend")
            return None, None
        
        print("\n🔍 Running FP-Growth Algorithm...")
        start_time = time.time()
        
        # Convert to DataFrame
        all_items = sorted(list(self.all_items))
        data = []
        for transaction in self.transactions:
            row = {item: (item in transaction) for item in all_items}
            data.append(row)
        df = pd.DataFrame(data)
        
        # Run FP-Growth
        frequent_itemsets_df = fpgrowth(df, min_support=min_support, use_colnames=True)
        
        if len(frequent_itemsets_df) > 0:
            frequent_itemsets_df['length'] = frequent_itemsets_df['itemsets'].apply(lambda x: len(x))
        
        elapsed = time.time() - start_time
        
        # Display results
        self.display_apriori_results(frequent_itemsets_df)
        
        # Generate rules
        if len(frequent_itemsets_df) > 0:
            try:
                rules_df = association_rules(frequent_itemsets_df, metric="confidence", min_threshold=min_confidence)
                self.display_apriori_rules(rules_df)
            except:
                print("\n  No association rules generated (need itemsets with 2+ items)")
                rules_df = None
        else:
            rules_df = None
        
        print(f"\n⏱️  Execution time: {elapsed:.4f} seconds")
        
        return frequent_itemsets_df, rules_df
    
    def display_frequent_itemsets(self, frequent_itemsets):
        """Display frequent itemsets"""
        self.print_section("FREQUENT ITEMSETS")
        
        total = sum(len(v) for v in frequent_itemsets.values())
        print(f"\n  Total frequent itemsets found: {total}")
        
        if total == 0:
            print("\n  💡 Tip: No frequent itemsets found. Try lowering the minimum support threshold.")
            print("     For example, use 0.2 (20%) or 0.1 (10%) instead.")
            return
        
        for k in sorted(frequent_itemsets.keys()):
            itemsets = frequent_itemsets[k]
            print(f"\n  📦 {k}-Itemsets ({len(itemsets)} found):")
            
            # Sort by support
            sorted_itemsets = sorted(itemsets, key=lambda x: x[1], reverse=True)
            
            # Show top 10
            for itemset, count in sorted_itemsets[:10]:
                support = count / self.num_transactions
                items_str = ', '.join(sorted(list(itemset)))
                print(f"     {{{items_str}}} - Count: {count}, Support: {support:.4f}")
            
            if len(sorted_itemsets) > 10:
                print(f"     ... and {len(sorted_itemsets) - 10} more")
    
    def display_apriori_results(self, df):
        """Display Apriori/FP-Growth results"""
        self.print_section("FREQUENT ITEMSETS")
        
        if len(df) == 0:
            print("\n  No frequent itemsets found.")
            return
        
        print(f"\n  Total frequent itemsets found: {len(df)}")
        
        for k in sorted(df['length'].unique()):
            k_itemsets = df[df['length'] == k].sort_values('support', ascending=False)
            print(f"\n  📦 {k}-Itemsets ({len(k_itemsets)} found):")
            
            # Show top 10
            for idx, row in k_itemsets.head(10).iterrows():
                items_str = ', '.join(sorted(list(row['itemsets'])))
                support = row['support']
                count = int(support * self.num_transactions)
                print(f"     {{{items_str}}} - Count: {count}, Support: {support:.4f}")
            
            if len(k_itemsets) > 10:
                print(f"     ... and {len(k_itemsets) - 10} more")
    
    def generate_rules(self, frequent_itemsets, min_confidence):
        """Generate association rules"""
        rules = []
        
        # Handle empty frequent_itemsets
        if not frequent_itemsets:
            return rules
        
        for k in range(2, max(frequent_itemsets.keys()) + 1):
            if k not in frequent_itemsets:
                continue
            
            for itemset, support_count in frequent_itemsets[k]:
                items = list(itemset)
                
                for i in range(1, len(items)):
                    for antecedent_items in combinations(items, i):
                        antecedent = frozenset(antecedent_items)
                        consequent = itemset - antecedent
                        
                        antecedent_support_count = self.get_support_count(antecedent)
                        
                        if antecedent_support_count == 0:
                            continue
                        
                        confidence = support_count / antecedent_support_count
                        
                        if confidence >= min_confidence:
                            support = support_count / self.num_transactions
                            consequent_support = self.get_support_count(consequent) / self.num_transactions
                            lift = confidence / consequent_support if consequent_support > 0 else 0
                            
                            rules.append({
                                'antecedent': antecedent,
                                'consequent': consequent,
                                'support': support,
                                'confidence': confidence,
                                'lift': lift
                            })
        
        return sorted(rules, key=lambda x: (x['confidence'], x['support']), reverse=True)
    
    def display_rules(self, rules):
        """Display association rules"""
        self.print_section("ASSOCIATION RULES")
        
        if not rules:
            print("\n  No association rules generated.")
            print("  💡 Tip: This can happen if:")
            print("     • No frequent itemsets were found (lower minimum support)")
            print("     • Itemsets don't meet minimum confidence threshold (lower it)")
            print("     • Only 1-itemsets were found (rules need 2+ items)")
            return
        
        print(f"\n  Total rules generated: {len(rules)}")
        print(f"\n  Top 15 rules:")
        print(f"\n  {'Rule':<50} {'Supp':>8} {'Conf':>8} {'Lift':>8}")
        print("  " + "-"*78)
        
        for rule in rules[:15]:
            ant_str = ', '.join(sorted(list(rule['antecedent'])))
            cons_str = ', '.join(sorted(list(rule['consequent'])))
            rule_str = f"{{{ant_str}}} → {{{cons_str}}}"
            print(f"  {rule_str:<50} {rule['support']:>8.4f} {rule['confidence']:>8.4f} {rule['lift']:>8.4f}")
        
        if len(rules) > 15:
            print(f"\n  ... and {len(rules) - 15} more rules")
    
    def display_apriori_rules(self, df):
        """Display Apriori/FP-Growth rules"""
        self.print_section("ASSOCIATION RULES")
        
        if df is None or len(df) == 0:
            print("\n  No association rules generated.")
            return
        
        print(f"\n  Total rules generated: {len(df)}")
        print(f"\n  Top 15 rules:")
        print(f"\n  {'Rule':<50} {'Supp':>8} {'Conf':>8} {'Lift':>8}")
        print("  " + "-"*78)
        
        sorted_rules = df.sort_values('confidence', ascending=False).head(15)
        
        for idx, rule in sorted_rules.iterrows():
            ant_str = ', '.join(sorted(list(rule['antecedents'])))
            cons_str = ', '.join(sorted(list(rule['consequents'])))
            rule_str = f"{{{ant_str}}} → {{{cons_str}}}"
            print(f"  {rule_str:<50} {rule['support']:>8.4f} {rule['confidence']:>8.4f} {rule['lift']:>8.4f}")
        
        if len(df) > 15:
            print(f"\n  ... and {len(df) - 15} more rules")
    
    def select_database(self):
        """Interactive database selection"""
        self.print_header("SELECT DATABASE")
        
        print("\nAvailable databases:\n")
        for key, (name, path, description) in self.databases.items():
            print(f"  {key}. {name:<12} - {description}")
        
        while True:
            choice = input("\nEnter database number (or 'q' to quit): ").strip()
            
            if choice.lower() == 'q':
                return None
            
            if choice in self.databases:
                return choice
            
            print("❌ Invalid choice. Please try again.")
    
    def select_algorithm(self):
        """Interactive algorithm selection"""
        self.print_header("SELECT ALGORITHM")
        
        print("\nAvailable algorithms:\n")
        for key, (name, _) in self.algorithms.items():
            print(f"  {key}. {name}")
        
        while True:
            choice = input("\nEnter algorithm number (or 'b' to go back): ").strip()
            
            if choice.lower() == 'b':
                return None
            
            if choice in self.algorithms:
                return choice
            
            print("❌ Invalid choice. Please try again.")
    
    def get_parameters(self):
        """Get mining parameters from user"""
        self.print_section("CONFIGURATION")
        
        while True:
            try:
                min_support = input("\n  Minimum support (0-1, default 0.2): ").strip()
                min_support = float(min_support) if min_support else 0.2
                
                if 0 <= min_support <= 1 or min_support >= 1:
                    break
                print("  ❌ Please enter a value between 0 and 1, or an integer.")
            except ValueError:
                print("  ❌ Invalid input. Please enter a number.")
        
        while True:
            try:
                min_confidence = input("  Minimum confidence (0-1, default 0.6): ").strip()
                min_confidence = float(min_confidence) if min_confidence else 0.6
                
                if 0 <= min_confidence <= 1:
                    break
                print("  ❌ Please enter a value between 0 and 1.")
            except ValueError:
                print("  ❌ Invalid input. Please enter a number.")
        
        return min_support, min_confidence
    
    def run(self):
        """Main interactive loop"""
        self.clear_screen()
        
        print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              📊 INTERACTIVE FREQUENT ITEMSET MINING TOOL 📊                   ║
║                                                                               ║
║          Analyze transactional databases using mining algorithms             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
        """)
        
        input("Press Enter to continue...")
        
        while True:
            self.clear_screen()
            
            # Select database
            db_choice = self.select_database()
            if db_choice is None:
                print("\n👋 Goodbye!")
                break
            
            db_name, db_path, db_desc = self.databases[db_choice]
            
            # Load database
            print(f"\n📂 Loading {db_name} database...")
            try:
                self.load_transactions(db_path)
                print(f"✓ Loaded {self.num_transactions} transactions with {len(self.all_items)} unique items")
            except FileNotFoundError:
                print(f"❌ Error: Database file not found at {db_path}")
                input("\nPress Enter to continue...")
                continue
            
            # Select algorithm
            algo_choice = self.select_algorithm()
            if algo_choice is None:
                continue
            
            algo_name, algo_func = self.algorithms[algo_choice]
            
            # Get parameters
            min_support, min_confidence = self.get_parameters()
            
            # Run mining
            self.print_header(f"{algo_name.upper()} - {db_name.upper()}")
            print(f"\n  Database: {db_name} ({db_desc})")
            print(f"  Transactions: {self.num_transactions}")
            print(f"  Unique Items: {len(self.all_items)}")
            print(f"  Min Support: {min_support}")
            print(f"  Min Confidence: {min_confidence}")
            
            algo_func(min_support, min_confidence)
            
            # Ask to continue
            print("\n" + "="*80)
            choice = input("\nOptions: [n]ew analysis, [q]uit: ").strip().lower()
            
            if choice == 'q':
                print("\n👋 Goodbye!")
                break


def main():
    """Entry point"""
    miner = InteractiveMiner()
    try:
        miner.run()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

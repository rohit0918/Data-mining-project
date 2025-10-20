# Interactive Frequent Itemset Mining

> **✨ NEW: Clean, organized structure with interactive terminal interface!**  
> All results displayed in terminal - no file clutter!

A comprehensive data mining project implementing three algorithms for frequent itemset mining and association rule discovery.

## 🎯 Features

- **Three Mining Algorithms:**
  - Brute Force (custom implementation)
  - Apriori (mlxtend library)
  - FP-Growth (mlxtend library)

- **Five Transactional Databases:**
  - Amazon (Technology)
  - BestBuy (Electronics)
  - Walmart (Groceries)
  - Target (Clothing)
  - Costco (Household)

- **Interactive Interface:**
  - User-friendly menu system
  - Real-time results display
  - Configurable parameters
  - No file clutter (results shown in terminal)

## 📁 Project Structure

```
Data mining/
├── main.py              # Interactive interface (START HERE)
├── data/                # Transaction databases (CSV files)
│   ├── Amazon_transactions.csv
│   ├── BestBuy_transactions.csv
│   ├── Walmart_transactions.csv
│   ├── Target_transactions.csv
│   └── Costco_transactions.csv
├── src/                 # Source code
│   ├── generate_databases.py
│   ├── brute_force_mining.py
│   ├── library_based_mining.py
│   └── run_brute_force.py
└── docs/                # Documentation
    ├── README.md
    ├── DATA_CREATION_REPORT.md
    ├── BRUTE_FORCE_ALGORITHM_REPORT.md
    ├── ALGORITHM_COMPARISON_REPORT.md
    └── ... (other reports)
```

## 📖 Getting Started

**👉 See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed walkthrough with examples!**

## 🚀 Quick Start

### Prerequisites

```bash
pip install mlxtend pandas numpy
```

### Run the Interactive Tool

```bash
python main.py
```

### What You'll See

1. **Welcome Screen** - Introduction to the tool
2. **Database Selection** - Choose from 5 databases
3. **Algorithm Selection** - Pick Brute Force, Apriori, or FP-Growth
4. **Configuration** - Set minimum support and confidence
5. **Results Display** - View frequent itemsets and association rules in terminal
6. **Repeat or Exit** - Run another analysis or quit

## 💡 Example Usage

```
SELECT DATABASE
1. Amazon      - Technology & Electronics
2. BestBuy     - Consumer Electronics
3. Walmart     - Groceries
4. Target      - Clothing & Fashion
5. Costco      - Household Items

Enter database number: 1

SELECT ALGORITHM
1. Brute Force
2. Apriori
3. FP-Growth

Enter algorithm number: 2

CONFIGURATION
Minimum support (0-1, default 0.2): 0.2
Minimum confidence (0-1, default 0.6): 0.6

[Results displayed in terminal...]
```

## 📊 Sample Output

```
FREQUENT ITEMSETS
  Total frequent itemsets found: 18

  📦 1-Itemsets (12 found):
     {HDMI_Cable} - Count: 10, Support: 0.4000
     {Router} - Count: 10, Support: 0.4000
     {USB_Cable} - Count: 10, Support: 0.4000
     ...

ASSOCIATION RULES
  Total rules generated: 15

  Top 15 rules:
  Rule                                                Supp     Conf     Lift
  {Laptop} → {Keyboard}                             0.2000   1.0000   5.0000
  {Mouse} → {Keyboard}                              0.2000   1.0000   5.0000
  ...
```

## 🔧 Advanced Usage

### Regenerate Databases

```bash
cd src
python generate_databases.py
```

This creates new deterministic transaction data in the `data/` folder.

### Run Individual Algorithms (Non-Interactive)

```bash
cd src

# Brute Force only
python run_brute_force.py

# Apriori + FP-Growth
python library_based_mining.py
```

## 📈 Parameters

### Minimum Support
- **Range:** 0.0 to 1.0 (percentage) or integer (absolute count)
- **Default:** 0.2 (20%)
- **Effect:** Lower = more itemsets found, slower execution

### Minimum Confidence
- **Range:** 0.0 to 1.0
- **Default:** 0.6 (60%)
- **Effect:** Lower = more rules generated

## 🎓 Educational Value

### Brute Force
- Shows exhaustive search approach
- Demonstrates exponential complexity
- Educational baseline for comparison

### Apriori
- Illustrates pruning optimization
- Uses downward closure property
- Standard industry algorithm

### FP-Growth
- Tree-based pattern growth
- Most efficient for large datasets
- Modern mining approach

## 📚 Documentation

Detailed reports are available in the `docs/` folder:

- **DATA_CREATION_REPORT.md** - How databases were created
- **BRUTE_FORCE_ALGORITHM_REPORT.md** - Brute force implementation details
- **ALGORITHM_COMPARISON_REPORT.md** - Performance comparison of all algorithms
- **QUICK_START_GUIDE.md** - Detailed usage instructions

## 🏆 Key Results

All three algorithms produce **identical results** (verified):
- ✅ Same frequent itemsets
- ✅ Same association rules
- ✅ Same support/confidence/lift values

### Performance (all 5 databases)
- **Brute Force:** 0.050s
- **Apriori:** 0.013s (3.85x faster)
- **FP-Growth:** 0.017s (2.94x faster)

## 🔍 Common Use Cases

### Product Bundling
Find items frequently bought together to create bundles.

### Store Layout
Place related products near each other based on co-occurrence.

### Recommendation Systems
Suggest items based on shopping cart contents.

### Inventory Management
Predict demand for complementary products.

## 🐛 Troubleshooting

### "mlxtend not found"
```bash
pip install mlxtend
```

### "File not found" error
Make sure you're running `main.py` from the project root directory.

### Database files missing
Run `python src/generate_databases.py` to recreate them.

## 📝 License

Educational project for data mining coursework.

## 👤 Author

Data Mining Project - Frequent Itemset Mining Implementation

---

**Start mining:** `python main.py` 🚀

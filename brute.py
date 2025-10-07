from itertools import combinations
from collections import defaultdict


def brute_force_apriori(transactions, min_support):
    """
    Brute force implementation of Apriori algorithm.
    min_support: minimum support threshold as a percentage (e.g., 0.15 for 15%)
    Returns:
    - frequent_itemsets: dict mapping k -> list of frequent k-itemsets
    - support_counts: dict mapping itemset -> support (as a fraction)
    """
    transactions = [set(t) for t in transactions]
    n_transactions = len(transactions)
    all_items = set()
    for transaction in transactions:
        all_items.update(transaction)
    all_items = sorted(all_items)

    print(f"Total items: {len(all_items)}")
    print(f"Total transactions: {n_transactions}")
    print(f"Minimum support: {min_support:.2f} ({min_support*100:.1f}%)\n")

    frequent_itemsets = {}
    support_counts = {}
    k = 1

    while True:
        print(f"--- Processing {k}-itemsets ---")
        candidates = list(combinations(all_items, k))
        n_candidates = len(candidates)
        print(f"Generated {n_candidates} possible {k}-itemsets")

        frequent_k = []
        for itemset in candidates:
            itemset_set = set(itemset)
            count = sum(1 for t in transactions if itemset_set.issubset(t))
            support = count / n_transactions
            if support >= min_support:
                frequent_k.append(itemset)
                support_counts[itemset] = support

        print(f"Found {len(frequent_k)} frequent {k}-itemsets")

        if len(frequent_k) == 0:
            print(f"\nNo frequent {k}-itemsets found. Terminating.\n")
            break

        frequent_itemsets[k] = frequent_k
        print()
        k += 1

    return frequent_itemsets, support_counts



def print_results(frequent_itemsets, support_counts):
    """Print the frequent itemsets and their support as percentages."""
    print("=" * 60)
    print("FREQUENT ITEMSETS")
    print("=" * 60)
    for k in sorted(frequent_itemsets.keys()):
        print(f"\n{k}-itemsets (count: {len(frequent_itemsets[k])}):")
        print("-" * 60)
        for itemset in frequent_itemsets[k]:
            support = support_counts[itemset]
            print(f"  {set(itemset)}: support = {support:.4f} ({support*100:.2f}%)")



# Read transactions
import ast
def read_transactions_from_file(filename):
    transactions = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.endswith(','):
                line = line[:-1]  # Remove trailing comma
            if line:
                transaction = ast.literal_eval(line)
                transactions.append(transaction)
    return transactions

if __name__ == "__main__":
    # Change this filename as needed
    filename = "trans5.txt"
    transactions = read_transactions_from_file(filename)
    print(f"Loaded {len(transactions)} transactions from {filename}")
 
    min_support = 0.15 #<------------------------------------ENTER MINIMUM SUPPORT HERE 

    # Run brute force apriori
    frequent_itemsets, support_counts = brute_force_apriori(transactions, min_support)

    # Print results
    print_results(frequent_itemsets, support_counts)

    # Summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total_frequent = sum(len(itemsets) for itemsets in frequent_itemsets.values())
    print(f"Total frequent itemsets found: {total_frequent}")
    print(f"Maximum itemset size: {max(frequent_itemsets.keys()) if frequent_itemsets else 0}")
    
    
    import time
start_time = time.time()
# Your script or code block
for i in range(1000000):
   pass
end_time = time.time()
print(f"Execution Time: {end_time - start_time} seconds")
from itertools import combinations
import ast

# Function to calculate support
def calculate_support(data, itemsets):
    support = {}
    for itemset in itemsets:
        count = sum(1 for transaction in data if set(itemset).issubset(transaction))
        support[itemset] = count / len(data)
    return support


# Generate candidate itemsets of size k
def generate_candidates(frequent_itemsets, k):
    items = set(item for itemset in frequent_itemsets for item in itemset)
    return [tuple(sorted(comb)) for comb in combinations(items, k)]

# Apriori Algorithm - Modified to return all frequent itemsets
def apriori(data, min_support):
    data = [set(transaction) for transaction in data]
    itemsets = [(item,) for transaction in data for item in transaction]
    itemsets = list(set(itemsets))
    
    all_frequent_itemsets = {}  # Store all frequent itemsets
    
    support = calculate_support(data, itemsets)
    frequent_itemsets = {itemset: sup for itemset, sup in support.items() if sup >= min_support}
    all_frequent_itemsets.update(frequent_itemsets)
        
    k = 2
    while frequent_itemsets:
        print(f"Frequent {k-1}-itemsets:")
        for itemset, sup in frequent_itemsets.items():
            print(f"{itemset}: {sup:.4f}")
        candidates = generate_candidates(frequent_itemsets.keys(), k)
        support = calculate_support(data, candidates)
        frequent_itemsets = {itemset: sup for itemset, sup in support.items() if sup >= min_support}
        all_frequent_itemsets.update(frequent_itemsets)
        k += 1
    
    return all_frequent_itemsets

# Generate Association Rules
def generate_association_rules(frequent_itemsets, data, min_confidence=0.7):
    rules = []
    
    # Only consider itemsets with more than 1 item for rules
    multi_item_sets = {itemset: support for itemset, support in frequent_itemsets.items() if len(itemset) > 1}
    
    for itemset, itemset_support in multi_item_sets.items():
        # Generate all possible antecedent-consequent combinations
        for i in range(1, len(itemset)):
            for antecedent in combinations(itemset, i):
                antecedent = tuple(sorted(antecedent))
                consequent = tuple(sorted(set(itemset) - set(antecedent)))
                
                if antecedent in frequent_itemsets and consequent in frequent_itemsets:
                    antecedent_support = frequent_itemsets[antecedent]
                    consequent_support = frequent_itemsets[consequent]
                    confidence = itemset_support / antecedent_support
                    
                    if confidence >= min_confidence:
                        rules.append({
                            'antecedents': antecedent,
                            'consequents': consequent,
                            'antecedent support': antecedent_support,
                            'consequent support': consequent_support,
                            'support': itemset_support,
                            'confidence': confidence
                        })
    
    return rules

# Print rules in table format similar to pandas output
def print_rules_table(rules):
    if not rules:
        print("No association rules found with the given confidence threshold.")
        return
    
    print("\nAssociation Rules:")
    print("=" * 100)
    print(f"{'antecedents':<25} {'consequents':<25} {'ant_support':<12} {'cons_support':<12} {'support':<10} {'confidence':<10}")
    print("-" * 100)
    
    for rule in rules:
        ant_str = "{" + ", ".join(rule['antecedents']) + "}"
        cons_str = "{" + ", ".join(rule['consequents']) + "}"
        print(f"{ant_str:<25} {cons_str:<25} {rule['antecedent support']:<12.4f} {rule['consequent support']:<12.4f} {rule['support']:<10.4f} {rule['confidence']:<10.4f}")
    
    print("=" * 100)

# Read dataset from trans1.txt <------------------------------------ Transactions source file
def read_dataset_from_file(filename):
    dataset = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.endswith(','):
                line = line[:-1]  # Remove trailing comma
            if line:
                transaction = ast.literal_eval(line)
                dataset.append(transaction)
    return dataset

dataset = read_dataset_from_file('trans1.txt')
print(f"Loaded {len(dataset)} transactions from trans1.txt")

print("DATASET:")
print("=" * 60)
for idx, transaction in enumerate(dataset):
    items = " | ".join(transaction)
    print(f"{idx+1:2d}. [{items}]")
    print("-" * 60)

# Run Apriori and get all frequent itemsets
print("\n" + "="*50)
print("APRIORI FREQUENT ITEMSETS")
print("="*50)
all_frequent_itemsets = apriori(dataset, min_support=0.15) #<------------------------------------ENTER MINIMUM SUPPORT HERE 

# Generate and display association rules
print("\n" + "="*50)
print("ASSOCIATION RULES GENERATION")
print("="*50)
rules = generate_association_rules(all_frequent_itemsets, dataset, min_confidence=0.7)#<------------------------------------ENTER MINIMUM CONFIDENCE HERE 
print_rules_table(rules)


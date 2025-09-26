import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

data = pd.read_csv('trans5_onehot.csv')
pd.set_option('display.max_rows', None)  # Show all rows
data = data.astype(bool)  # Convert 0/1 to True/False
print(data)

# Find frequent itemsets with a minimum support of 0.15
frequent_itemsets = apriori(data, min_support=0.15, use_colnames=True)
print(frequent_itemsets)

# Generate rules with a minimum confidence of 0.7
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
print(rules[['antecedents', 'consequents', 'antecedent support', 'consequent support', 'support', 'confidence']])

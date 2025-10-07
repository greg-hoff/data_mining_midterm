import pandas as pd

# Example one-hot encoded DataFrame
data = pd.read_csv('trans1_onehot.csv')
pd.set_option('display.max_rows', None)  # Show all rows
data = data.astype(bool)  # Convert 0/1 to True/False

df = pd.DataFrame(data)

# Convert one-hot encoded DataFrame to transaction list
transaction_list = df.apply(lambda row: [col for col in df.columns if row[col] == 1], axis=1).tolist()

for transaction in transaction_list:
    # Convert all items to strings and add quotes around each item
    string_items = [f"'{str(item)}'" for item in transaction]
    items = ', '.join(string_items)
    print(f"[{items}],")

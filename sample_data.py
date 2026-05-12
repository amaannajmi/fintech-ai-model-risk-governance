# -*- coding: utf-8 -*-
# This script takes 5,000 rows from the full dataset
# and saves them as a smaller sample for GitHub

import pandas as pd

# Load the full dataset
df = pd.read_csv("data/creditcard.csv")

# Take 5,000 rows — keeping the fraud ratio realistic
sample = df.sample(n=5000, random_state=42)

# Save it
sample.to_csv("data/sample.csv", index=False)

print(f"Sample created: {len(sample)} rows")
print(f"Fraud cases in sample: {sample['Class'].sum()}")
"""
Transform To:

{
    "A": {"North": 30, "South": 25, "West": 20},
    "B": {"North": 20, "East": 10, "West": 25},
    "C": {"South": 15, "East": 5}
}
"""

import json
from collections import defaultdict

product_freq = defaultdict(lambda: defaultdict(int))

with open('products.json', 'r') as f:
    
    reader = json.load(f)

    for line in reader:
        
        region = line["region"]
        sales = line["sales"]

        for sale in sales:
            p = sale["product"]
            q = sale["quantity"]

            product_freq[p][region] += q


# Convert defaultdict to normal dict before saving
final_data = {product: dict(regions) for product, regions in product_freq.items()}

# save dict in file
with open('products-transformed.json', 'w') as wf:
    json.dump(final_data, wf, indent=4)
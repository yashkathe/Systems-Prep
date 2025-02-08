import re
from collections import defaultdict

file = 'q4.txt'

bit_freq = defaultdict(int)

with open(file, 'r') as rf:
   
    pattern= re.compile(r'([0-1]{4})')

    for line in rf:
        for bit in pattern.findall(line):
            bit_freq[bit] += 1

for k, v in bit_freq.items():
    print(k, v)
import re
from collections import defaultdict

email_freq = defaultdict(int)

with open('./para.txt', 'r') as r:

    # option 1
    # pattern = re.compile(r'[a-zA-Z.0-9_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+')

    # option 2
    pattern = re.compile(r'[\w\.\d_]+@[\w\\d_]+\.[\w\\d_]+')


    for line in r:
        for email in pattern.findall(line):

            email_freq[email] += 1

for k, v in sorted(email_freq.items(), reverse=True, key = lambda x: x[1]):
    print(k, v)

"""
support@example.com 3
sales@business.co 2
john.doe@gmail.com 1
jane_doe123@yahoo.com 1
marketing@company.org 1
"""
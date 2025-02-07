import re

"""
Write a regex pattern to match all words that contain an underscore (_).
"""

with open('q1.txt', 'r') as f:

    pattern = re.compile(r'[\w]+_[\w]+')

    for line in f:
        for match in pattern.findall(line):
            print(match)

"""
cat_dog
hello_world
regex_test
fun_with_regex
ABCD_efgh
"""


"""
Write a regex pattern to match all numbers that have exactly 4 digits.
"""

with open('q1.txt', 'r') as f:

    pattern = re.compile(r'\d{4}')

    for line in f:
        for match in pattern.findall(line):
            print(match)
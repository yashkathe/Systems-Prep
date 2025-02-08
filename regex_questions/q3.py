"""
Parse the file and extract all failed test cases along with their timestamps.
Save the output in a new file called failed_tests.txt with this format:

TEST_CASE_2: 2025-01-14 10:20:45
TEST_CASE_3: 2025-01-14 10:22:00
TEST_CASE_5: 2025-01-14 10:30:00
"""

data = """
[2025-01-14 10:15:30] TEST_CASE_1: PASS
[2025-01-14 10:20:45] TEST_CASE_2: FAIL
[2025-01-14 10:22:00] TEST_CASE_3: FAIL
[2025-01-14 10:25:15] TEST_CASE_4: PASS
[2025-01-14 10:30:00] TEST_CASE_5: FAIL
"""

import re

pattern = re.compile(r'\[(.*?)\](.*?): FAIL')

for line in pattern.findall(data):
    print(line[0], line[1])

with open('q3.txt', 'w') as rf:
    for line in pattern.findall(data):
        rf.write(f'{line[1]} : {line[0]}'.strip())
        rf.write('\n')
"""
Write a Python function to:

Parse the log file and categorize the results into PASS and FAIL.
Save the results into two separate files, pass_logs.txt and fail_logs.txt.
"""

f1 = "q1_w_pass"
f2 = "q1_w_fail"

import re

with open('q5.txt', 'r') as rf:
    with open(f1, 'a') as w1:
        with open(f2, 'a') as w2:

            pattern = re.compile(r'(.*).(PASS|FAIL)')

            for line in rf:
                for matches in pattern.findall(line):
                    log, res = matches[0], matches[1]
                    
                    if res == 'PASS':
                        w1.write('{}\n'.format(log))
                    else:
                        w2.write('{}\n'.format(log))
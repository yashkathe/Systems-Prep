"""
Identify parameters that have changed values between config_old.csv and config_new.csv.
List parameters that exist in config_new.csv but are missing from config_old.csv.
Find parameters that were removed from config_new.csv but were present in config_old.csv.
Generate a summary report of all configuration differences.
Determine which category (CATEGORY) had the most modifications.
"""

import csv
from collections import defaultdict

#----------------------------------------------------------------------------------------# 
# Identify parameters that have changed values between config_old.csv and config_new.csv #
#----------------------------------------------------------------------------------------# 

changed_params = set()

with open('./config_new.csv', 'r') as r1, open('./config_old.csv', 'r') as r2:

    reader1 = csv.reader(r1)
    reader2 = csv.reader(r2)

    next(reader1)
    next(reader2)

    for lines in zip(reader1,reader2):
        
        parameter = lines[0][0]

        if lines[0] != lines[1]:
            changed_params.add(parameter)

print('changed parameters are {}'.format(changed_params))




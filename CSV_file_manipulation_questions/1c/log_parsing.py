"""
Count the number of occurrences for each LOG_LEVEL.
Extract and display all unique error messages along with their first occurrence TIMESTAMP.
Identify the time periods with the highest frequency of ERROR logs.
"""

import csv
from collections import defaultdict

#----------------------------------------------------# 
# Count the number of occurrences for each LOG_LEVEL #
#----------------------------------------------------#

freq_logs = defaultdict(int)

with open('./application_logs.csv', 'r') as r:

    reader = csv.DictReader(r)

    for line in reader:

        log_lvl = line['LOG_LEVEL']
        freq_logs[log_lvl] += 1
        
print(freq_logs)

#-------------------------------------------------------------------------------------------#
# Extract and display all unique error messages along with their first occurrence TIMESTAMP #
#-------------------------------------------------------------------------------------------#

err_msgs = dict()

with open('./application_logs.csv', 'r') as r:

    reader = csv.DictReader(r)

    for line in reader:

        err = line['MESSAGE']

        if err not in err_msgs:

            time_stamp = line['TIMESTAMP']
            err_msgs[err] = time_stamp

print(err_msgs)

#--------------------------------------------------------------------#
# Identify the time periods with the highest frequency of ERROR logs #
#--------------------------------------------------------------------#

freq_error_times = defaultdict(int)

with open('./application_logs.csv', 'r') as r:

    reader = csv.DictReader(r)

    for line in reader:

        log_lvl = line['LOG_LEVEL']

        if log_lvl == 'ERROR':

            time_stamp = line['TIMESTAMP']

            freq_error_times[time_stamp] += 1 

print(freq_error_times)

# Find max frequency
max_freq = max(freq_error_times.values())

# Get all timestamps with max frequency
max_timestamps = [ts for ts, freq in freq_error_times.items() if freq == max_freq]
